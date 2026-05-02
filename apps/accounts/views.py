from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import EmailAuthenticationForm, ParentRegistrationForm, StudentRegistrationForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm


class UserLogoutView(LogoutView):
    pass


class StudentRegisterView(FormView):
    form_class = StudentRegistrationForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect('core:dashboard')


class ParentRegisterView(FormView):
    form_class = ParentRegistrationForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect('core:dashboard')
