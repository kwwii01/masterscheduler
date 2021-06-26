from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login')
]
