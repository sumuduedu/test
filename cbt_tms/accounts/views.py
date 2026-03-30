from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LogoutView):
    pass


@login_required
def dashboard(request):
    user = request.user
    context = {'role': user.role}
    template_map = {
        'ADMIN': 'accounts/dashboard_admin.html',
        'TRAINER': 'accounts/dashboard_trainer.html',
        'STUDENT': 'accounts/dashboard_student.html',
        'ASSESSOR': 'accounts/dashboard_assessor.html',
    }
    return render(request, template_map.get(user.role, 'accounts/dashboard_student.html'), context)


def home(request):
    return render(request, 'accounts/home.html')
