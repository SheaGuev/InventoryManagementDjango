from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("?<str:query>", views.search, name="search"),
    path("reservations", views.reservations, name="reservations")
]
