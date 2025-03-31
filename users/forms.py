from django import forms

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from phonenumber_field.formfields import PhoneNumberField

from users.models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=PasswordInput)
    confirm_password = forms.CharField(widget=PasswordInput)
    phone_number = PhoneNumberField(region='UZ', required=False)
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        email_check = CustomUser.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('This Email already exists')

        if len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        cleaned_data["password"] = make_password(password)
        return cleaned_data
