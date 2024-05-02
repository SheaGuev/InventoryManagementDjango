from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Changed from 'index' to 'home'
    path("equipment/", views.equipment, name="equipment"),
    path("search/", views.search_view, name="search"),

    path("?<str:query>", views.search_view, name="search"), # Allows search on the home page
    path("reservations/", views.reservations, name="reservations"),
    path("requests/", views.equipmentRequests, name="requests"),
    path('device/<str:device_serial>/', views.device_view, name='device_view'),
    path('device/<str:device_serial>/edit/', views.edit_device, name='edit_device'),
    path('add_device/', views.add_device, name='add_device'),


    path("reports/", views.reports, name="reports")
]
