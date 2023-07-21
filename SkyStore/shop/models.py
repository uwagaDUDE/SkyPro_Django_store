from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

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
    versions = models.CharField(default='')

    def __str__(self):
        return self.name


