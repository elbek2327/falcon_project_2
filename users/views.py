from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
# from django.core.mail import send_mail
from users.forms import LoginForm, RegisterForm
from users.models import CustomUser
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

# Create your views here.


        

class LoginView(FormView):
    template_name = 'users/simple/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('shop:index')

    def form_valid(self, form):
        user = authenticate(self.request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, "Login successful!")
                return super().form_valid(form)
            else:
                messages.error(self.request, "Please verify your email first.")
        else:
            messages.error(self.request, "Invalid email or password")
        return self.form_invalid(form)


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



def register_view(request):
    if request.method == "POST":
        next_thing = request.GET.get('next_thing')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            #avtomatik save qiladi verification link borgan payti
            user.save()
            user.is_active = True
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)

            if next_thing:
                return redirect(next_thing)
            else:
                return redirect('users:verify_email')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/simple/register.html', context)
# send email with verification link
def verify_email(request):
    if request.method == "POST":
        if request.user.is_authenticated and isinstance(request.user, CustomUser) and request.user.email:
            if not request.user.email_is_verified:
                current_site = get_current_site(request)
                user = request.user
                email = request.user.email
                subject = "Verify Email"
                message = render_to_string('users/verification_email/verify_email_message.html', {
                    'request': request,
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                email = EmailMessage(
                    subject, message, to=[email]
                )
                email.content_subtype = 'html'
                email.send()
                return redirect('users:verify_email_done')
        else:
            return redirect('users:register_page')
    return render(request, 'users/verification_email/verify_email.html')


def verify_email_done(request):
    return render(request, 'users/verification_email/verify_email_done.html')

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        user.is_active = True
        user.email_is_verified = True
        messages.success(request, 'Your email has been verified.')
        return redirect('users:verify_email_complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'users/verification_email/verify_email_confirm.html')

def verify_email_complete(request):
    return render(request, 'users/verification_email/verify_email_complete.html')

