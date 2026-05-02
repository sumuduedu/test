from django.urls import path

from .views import (
    CourseBuilderWizardView,
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseListView,
    CourseUpdateView,
    LessonPlanBuilderView,
    LessonPlanPDFView,
    lessonplan_options,
    module_options,
    task_options,
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('lesson-plans/<int:pk>/builder/', LessonPlanBuilderView.as_view(), name='lessonplan_builder'),
    path('lesson-plans/<int:pk>/pdf/', LessonPlanPDFView.as_view(), name='lessonplan_pdf'),
    path('builder/step/<int:step>/', CourseBuilderWizardView.as_view(), name='course_builder'),
    path('builder/step/<int:step>/<int:pk>/', CourseBuilderWizardView.as_view(), name='course_builder'),
    path('api/modules/<int:course_id>/', module_options, name='module_options'),
    path('api/tasks/<int:module_id>/', task_options, name='task_options'),
    path('api/lessonplans/<int:task_id>/', lessonplan_options, name='lessonplan_options'),
]
