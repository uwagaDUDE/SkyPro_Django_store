from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.db import models
from datetime import datetime

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за ед. продукта')
    description = models.TextField(max_length=1800, verbose_name='Описание товара')
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

class ProductVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за ед. продукта')
    description = models.TextField(max_length=1800, verbose_name='Описание товара')
    created_at = models.DateTimeField(default=datetime.now)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name