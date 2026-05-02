from django.urls import path
from . import views

urlpatterns = [
    path('', views.batch_list, name='batch_list'),
    path('create/', views.batch_create, name='batch_create'),
    path('enroll/', views.enrollment_create, name='enrollment_create'),
    path('session/', views.session_list, name='session_list'),
    path('session/create/', views.session_create, name='session_create'),
    path('timetable/create/', views.timetable_create, name='timetable_create'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('progress/', views.progress_overview, name='progress_overview'),
]
