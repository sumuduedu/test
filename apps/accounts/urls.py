from django.urls import path
from .views import ParentRegisterView, StudentRegisterView, UserLoginView, UserLogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/student/', StudentRegisterView.as_view(), name='register_student'),
    path('register/parent/', ParentRegisterView.as_view(), name='register_parent'),
]
