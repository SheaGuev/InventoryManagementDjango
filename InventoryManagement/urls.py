from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search_view, name="search"),
    path('device/<str:device_serial>/', views.device_view, name='device_view'),

]
