from django.urls import path
from . import views

urlpatterns = [
    path('labs/', views.lab_list, name='lab_list'),
    path('labs/create/', views.lab_create, name='lab_create'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('materials/create/', views.material_create, name='material_create'),
]
