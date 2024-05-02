from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_request, name="register"),
    path('', views.login_request, name="login"),
    path('placeholder/', views.placeholder, name='placeholder'),
    path('list_users/', views.list_users, name='list_users'),

    ##below need to be swapped out
    # path('admin_home/', views.admin_home, name='admin_home'),
    # path('user_home/', views.user_home, name='user_home'),
    # other paths...
]