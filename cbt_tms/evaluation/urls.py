from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/create/', views.feedback_create, name='feedback_create'),
    path('trainer/create/', views.trainer_evaluation_create, name='trainer_evaluation_create'),
    path('performance/', views.batch_performance_dashboard, name='batch_performance_dashboard'),
]
