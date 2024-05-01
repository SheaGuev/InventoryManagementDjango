from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Changed from 'index' to 'home'
    path("equipment/", views.equipment, name="equipment"),
    path("search/", views.search_view, name="search"),
    path('device/<str:device_serial>/', views.device_view, name='device_view'),
    path('device/<str:device_serial>/edit/', views.edit_device, name='edit_device'),

]
