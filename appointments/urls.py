from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_appointment, name='create'),
    path('<int:appointment_id>/', views.details, name='details'),
    path('<int:appointment_id>/cancel', views.cancel_appointment, name='cancel_appointment'),
    path('<str:appointment_status>/', views.filtered_by_status, name='filtered_by_status'),

    path('ajax/load-masters/', views.load_masters, name='ajax_load_masters'),
    path('ajax/load-workschedule', views.load_workschedule, name='ajax_load_workschedule'),
]
