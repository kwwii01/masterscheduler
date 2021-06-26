from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('create/', views.create_appointment, name='create'),

    path('ajax/load-masters/', views.load_masters, name='ajax_load_masters'),
    path('ajax/load-workschedule', views.load_workschedule, name='ajax_load_workschedule'),
]
