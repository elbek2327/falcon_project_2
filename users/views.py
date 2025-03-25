from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, RedirectView
from django.core.mail import send_mail
from users.forms import LoginForm, RegisterForm
from users.models import CustomUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

# Create your views here.


# def login_page(request):
#     form = LoginForm()
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             cd = form.cleaned_data
#             print(f"Form Data: {cd}")
#
#             user = authenticate(request, email=cd['email'], password=cd['password'])
#             print(f"Authenticated User: {user}")
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     messages.success(request, "Login successful!")
#                     return redirect('shop:index')
#                 else:
#                     messages.error(request, 'Disabled account')
#             else:
#                 messages.error(request, 'Invalid email or password')
#
#     return render(request, 'users/simple/login.html', {'form': form})


class LoginView(FormView):
    template_name = 'users/simple/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('shop:index')

    def form_valid(self, form):
        cd = form.cleaned_data
        print(f" Form Data: {cd}")

        user = authenticate(self.request, email=cd['email'], password=cd['password'])
        print(f"Authenticated User: {user}")

        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, "Login successful!")
                return super().form_valid(form)
            else:
                messages.error(self.request, " Disabled account")
        else:
            messages.error(self.request, " Invalid email or password")

        return self.form_invalid(form)




# def register_page(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = CustomUser.objects.create(
#                 email=form.cleaned_data['email'],
#                 first_name=form.cleaned_data['name'],
#                 password=form.cleaned_data['password'],
#             )
#             user.save()
#             messages.success(request, 'Registration successful. Please login.')
#             return redirect('users:login_page')
#
#     return render(request, 'users/simple/register.html', {'form': form})

class RegisterView(FormView):
    template_name = 'users/simple/register.html'
    success_url = reverse_lazy('users:login_page')
    form_class = RegisterForm

    def form_valid(self, form):
        user = CustomUser.objects.create_user(
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['name'],
            password=form.cleaned_data['password']
        )
        # user.save()
        messages.success(self.request, "Registration successful. Please login.")
        send_mail(
            'Hello Dear!',
            'You Successfully registered',
            'zubaydullayev1609@gmail.com',
            [user.email],
            fail_silently=False
        )
        return super().form_valid(form)

class LogoutView(RedirectView):
    url = reverse_lazy('shop:index')

    def dispatch(self, request, *args, **kwargs):

        logout(request)
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

def github_login_redirect(request):
    """Redirect to GitHub login using Django-Allauth."""
    return redirect('/accounts/github/login/')

def google_login_redirect(request):
    return redirect('/accounts/login/')



