from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_list, name='assessment_list'),
    path('create/', views.assessment_create, name='assessment_create'),
    path('performance-guide/create/', views.performance_guide_create, name='performance_guide_create'),
    path('product-rating/create/', views.product_rating_create, name='product_rating_create'),
    path('attitude/create/', views.attitude_evaluation_create, name='attitude_evaluation_create'),
    path('evidence/create/', views.evidence_create, name='evidence_create'),
    path('competency/create/', views.competency_result_create, name='competency_result_create'),
    path('competency/', views.competency_result_list, name='competency_result_list'),
]
