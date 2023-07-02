from django import forms
from shop.models import Product, ProductVersion

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductVersionForm(forms.ModelForm):
    version = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version'].choices = [(version, version) for version in self.instance.versions]

    class Meta:
        model = ProductVersion
        fields = '__all__'