from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),  # Changed from 'index' to 'home'
    path("equipment/", views.equipment, name="equipment"),
    path("search/", views.search_view, name="search"),

    path("?<str:query>", views.search_view, name="search"), # Allows search on the home page
    path("reservations/", views.reservations, name="reservations"),
    path("requests/", views.equipmentRequests, name="requests"),
    path('device/<str:device_serial>/', views.device_view, name='device_view'),
    path('device/<str:device_serial>/edit/', views.edit_device, name='edit_device'),
    path('add_device/', views.add_device, name='add_device'),


    path("reports/", views.reports, name="reports"),


    # Harsh's URLs
    path('admin_home/', views.admin_home, name='admin_home'),
    path('user_home/', views.user_home, name='user_home'),
    path('logout/', views.custom_logout, name='logout'),
    path('make_admin/<int:user_id>/', views.make_admin, name='make_admin'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('make_user/<int:user_id>/', views.make_user, name='make_user'),
]
