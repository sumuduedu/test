from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class TailwindMixin:
    def _apply_classes(self):
        base = 'w-full rounded-xl border border-white/30 bg-white/70 px-10 py-3 text-slate-800 placeholder-slate-500 outline-none transition focus:ring-2 focus:ring-indigo-500'
        for _, field in self.fields.items():
            field.widget.attrs['class'] = base


class EmailAuthenticationForm(TailwindMixin, AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_classes()


class StudentParentRegistrationForm(TailwindMixin, UserCreationForm):
    role = forms.ChoiceField(choices=(('student', 'Student'), ('parent', 'Parent')))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_classes()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.is_active = False
        if commit:
            user.save()
        return user


class ProfileUpdateForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_classes()
