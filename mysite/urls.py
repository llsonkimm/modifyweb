from django.urls import path
from django.contrib import admin
from django.views.generic import RedirectView

from mysite.core import views

from django.conf import settings
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('trial1/', views.CustomFieldFormView.as_view(), name='trial_1'),
    path('trial2/', views.CustomBusinessFieldFormView.as_view(), name='trial_2'),
    path('trial3/', views.CustomNeedsFieldFormView.as_view(), name='trial_3'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('confirm-email/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm_email'),
     path(
    'reset-password/',
    auth_views.PasswordResetView.as_view(
      template_name='reset_password.html',
      html_email_template_name='reset_password_email.html',
      success_url=settings.LOGIN_URL,),
    name='reset_password'
  ),
  path(
    'reset-password-confirmation/<str:uidb64>/<str:token>/',
    auth_views.PasswordResetConfirmView.as_view(
      template_name='reset_password_update.html', 
      post_reset_login=True,
      post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
    
      success_url=settings.LOGIN_REDIRECT_URL),
    name='password_reset_confirm'
  ),
]
