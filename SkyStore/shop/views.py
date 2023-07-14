from .models import Product
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from shop.models import Product, ProductVersion, User
from shop.forms import ProductForm, ProductVersionForm, RegistrationForm

def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/activation_invalid.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Подтверждение адреса электронной почты'
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('registration_activation_sent')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def home(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'shop/home.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            # Создаем версию товара
            version = ProductVersion(product=product, name=form.cleaned_data['name'], price=form.cleaned_data['price'],
                                     description=form.cleaned_data['description'])
            version.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    versions = ProductVersion.objects.filter(product_id=pk)
    old_versions = versions

    # Создаем formset для редактирования версий продукта
    ProductVersionFormSet = modelformset_factory(ProductVersion, fields=('name', 'price', 'description'), extra=1)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductVersionFormSet(request.POST, queryset=versions)
        if form.is_valid() and formset.is_valid():
            # Сохраняем изменения в основной модели
            form.save()
            # Сохраняем изменения в версиях продукта
            for version_form in formset:
                if version_form.is_valid():
                    version_form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductVersionFormSet(queryset=versions)

    return render(request, 'shop/edit_product.html',
                  {'form': form, 'product': product, 'formset': formset, 'old_versions': old_versions})

def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'shop/all_products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})