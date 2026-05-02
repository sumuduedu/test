from django.urls import path
from .views import CourseCreateView, CourseDeleteView, CourseListView, CourseUpdateView

app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('create/', CourseCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='delete'),
]
