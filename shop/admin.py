from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html  # image uchun
from shop.models import Product, Category, Images, Customers

admin.site.unregister(Group)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'address', 'created_at','customer_image', 'vat_number')

    def customer_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 30px;" max-height: 30px; border-radius: 50%; object-fit: cover;" />',
                obj.image.url)
        else:
            return 'No image found'

    customer_image.short_description = 'Customer Image'  # Column name
