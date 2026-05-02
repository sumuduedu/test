from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView

from .forms import EmailAuthenticationForm, ProfileUpdateForm, StudentParentRegistrationForm


class RoleDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


class SecureLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class SecureLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class RegisterView(CreateView):
    form_class = StudentParentRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:activation-sent')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created. Please wait for admin activation.')
        return response


class ActivationSentView(TemplateView):
    template_name = 'accounts/activation_sent.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


class HomeRedirectView(TemplateView):
    template_name = 'accounts/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return redirect('accounts:login')
