from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user


class ParentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.PARENT
        if commit:
            user.save()
        return user
