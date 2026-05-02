from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import (
    ActivationSentView,
    HomeRedirectView,
    ProfileView,
    RegisterView,
    RoleDashboardView,
    SecureLoginView,
    SecureLogoutView,
)

app_name = 'accounts'

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='home'),
    path('login/', SecureLoginView.as_view(), name='login'),
    path('logout/', SecureLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activation-sent/', ActivationSentView.as_view(), name='activation-sent'),
    path('dashboard/', RoleDashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', success_url=reverse_lazy('accounts:dashboard')), name='password-change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', email_template_name='registration/password_reset_email.html', success_url=reverse_lazy('accounts:password-reset-done')), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password-reset-done'),
]
