from users.views import LogoutView, LoginView

from django.urls import  include
app_name = 'users'

from django.urls import path
# from shop import views
from users import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page'),
    path('register/', views.register_view, name='register_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path("auth/", include("social_django.urls", namespace="social")),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_email/done/', views.verify_email_done, name='verify_email_done'),
    path('verify_email_confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify_email_confirm'),
    path('verify_email_complete/', views.verify_email_complete, name='verify_email_complete'),

]
