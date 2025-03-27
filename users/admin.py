from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from jazzmin.templatetags.jazzmin import User

from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'password', 'is_staff')