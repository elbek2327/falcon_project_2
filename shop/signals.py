# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db import models

from shop.models import Customers
from users.models import CustomUser
# import json



# Customer create bolganida terminalda xabar beradi
@receiver(post_save, sender=Customers)
def create_customer(sender, instance, created, **kwargs):
    users = CustomUser.objects.filter(is_superuser=True) #adminga yuborish uchun
    if created:
        print("************===**********")
        print(f"The user {instance.name}'s vat number: {instance.vat_number} successfully created!")
        print("************===**********")
        send_mail(
            f"Hello, there",
            f'Customer {instance.name} is now created!. \n{instance.vat_number} is vat number of customer' ,
            'zubaydullayev1609@gmail.com',
            [user.email for user in users],
        )


# bu modelda ozgarish bolsa bildiradi
@receiver(pre_save)  # agar bitta model uchun bolganida bitta modelni olardim senderga nu hammasi kk oshanga yozilmadi
def notify_model_changes_admin(sender, instance, **kwargs):
    if not isinstance(sender, models.Model) or sender._meta.app_label in ['contenttypes', 'sessions', 'admin', 'auth']:
        return

        # Get all superusers (admins)

    superusers = CustomUser.objects.filter(is_superuser=True) #adminlarni bilish uchun kerak data olinadi filter qilinib
    admin_emails = [admin.email for admin in superusers if admin.email] #bu admin emaillar message send qilish uchn kerak

    if not admin_emails:
        return #none



    try:
        old_instance = sender.objects.get(pk=instance.pk)
        changes = [] #ozgarishlarni saqlab turish
        for field in sender._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name, None)
            new_value = getattr(instance, field_name, None)
            if old_value != new_value:
                changes.append(f"{field_name}: '{old_value}' → '{new_value}'")

        if changes:
            action = f"Updated {sender.__name__} (ID: {instance.pk})"
            message = f"Changes:\n" + "\n".join(changes)
        else:
            return  # xech nima real change bolmasa otkazib yuboradi

    except sender.DoesNotExist:
        '''Bu yerda message ketadi usersga nima haqidaligi'''
        action = f"Created a new {sender.__name__}" #user kimdir nimadir create qildi actioni
        message = f"New record:\n" + "\n".join(
            [f"{field.name}: {getattr(instance, field.name)}" for field in sender._meta.fields])
        '''xabari'''

    # email xabari  va egasai subjecti
    subject = f"Model Change: {action}"
    full_message = f"Admin ,\n\n{action}\n\n{message}\n\nxurmat bilan, Django auto signali"

    # if user is is_superuser it will send emails to them ularga yuboradi
    if admin_emails:
        send_mail(subject, full_message, settings.DEFAULT_FROM_EMAIL, admin_emails)
















