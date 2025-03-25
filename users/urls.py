from users.views import RegisterView, LogoutView, LoginView

from django.urls import  include
app_name = 'users'

from django.urls import path
# from shop import views
from users import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page'),
    path('register/', RegisterView.as_view(), name='register_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path("auth/", include("social_django.urls", namespace="social")),
]
