from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search_view, name="search"),
    path('device?serial=<str:device_serial>', views.device_view, name='device_view'),
    
    path("?<str:query>", views.search_view, name="search"), # Allows search on the home page
    path("reservations", views.reservations, name="reservations"),
    path("requests", views.equipmentRequests, name="requests")
]
