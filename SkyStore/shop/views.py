from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product, ProductVersion
from shop.forms import ProductForm, ProductVersionForm



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
    versions = ProductVersion.objects.filter(product_id=pk).order_by('-version')
    old_version = versions.first()  # Получаем первую (старую) версию товара

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'shop/edit_product.html', {'form': form, 'product': product, 'versions': versions, 'old_version': old_version})

def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'shop/all_products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})