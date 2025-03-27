# from socket import send_fds
# import uuid
import random

from django.db import models
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"




class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            self.discount_price = self.price * Decimal(1 - self.discount / 100)
            return Decimal(f"{self.discount_price}").quantize(Decimal("0.00"))
        return Decimal(f'{self.price}').quantize(Decimal('0.00'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'


class Images(models.Model):
    image = models.ImageField(upload_to='product/images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} {self.image.url}"

    class Meta:
        verbose_name_plural = 'Images'


class Customers(models.Model):
    name = models.CharField(max_length=155, blank=True, null=True)
    email = models.EmailField()
    phone_number = PhoneNumberField(region='UZ')
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(upload_to='customer/images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vat_number = models.CharField(max_length=15, editable=False)

    def save(self, *args, **kwargs):
        if not self.vat_number:
            self.vat_number = self.generate_unique_vat()
        super().save(*args, **kwargs)

    def generate_unique_vat(self):
        """10 lik unique vat generator"""
        while True:
            vat = str(random.randint(1000000000, 9999999999))
            if not Customers.objects.filter(vat_number=vat).exists():
                return vat



    def __str__(self):
        return f" Name - {self.name} email - {self.email} - {self.vat_number}"
    class Meta:
        verbose_name_plural = 'Customers'
