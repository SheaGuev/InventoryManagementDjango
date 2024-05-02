# from django.shortcuts import render, redirect
#
# from InventoryManagement.models import CustomUser
# from .forms import NewUserForm, LoginForm
# from django.contrib.auth import login, authenticate
# from django.contrib import messages
# import logging
# # from InventoryManagement.models import CustomUser
# from django.contrib.auth.decorators import login_required
# from InventoryManagement import urls
#
# @login_required
# def user_home(request):
#     return render(request, 'user_home.html')
#
# @login_required
# def admin_home(request):
#     return render(request, 'admin_home.html')
#
#
# logger = logging.getLogger(__name__)
#
# def register_request(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             try:
#                 user = form.save()
#                 login(request, user)
#                 logger.info('User registered successfully. Email: %s', user.email)
#                 messages.success(request, "Registration successful.")
#                 return redirect("login")  # Redirect to the login page
#             except Exception as e:
#                 logger.error('Error during user creation: %s', str(e))
#                 messages.error(request, "Unsuccessful registration. Error during user creation.")
#         else:
#             logger.warning('Unsuccessful registration. Form errors: %s', form.errors)
#             messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = NewUserForm()
#     return render(request=request, template_name="registration.html", context={"register_form": form})
#
# def login_request(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 logger.info('User authenticated, redirecting to placeholder page.')
#                 if user.role.role_name == 'admin':
#                     return redirect("admin_home")  # Redirect to the admin home page
#                 else:
#                     return redirect("user_home")  # Redirect to the user home page
#             else:
#                 logger.warning('Invalid email or password. Email: %s', email)
#                 messages.error(request, "Invalid email or password.")
#     else:
#         form = LoginForm()
#     return render(request, "login.html", {"form": form})
#
#
# class UserForm:
#     pass
#
#
# def placeholder(request):
#     return render(request, 'placeholder.html')
#
#
# def list_users(request):
#     users = CustomUser.objects.all()
#     return render(request, 'list_users.html', {'users': users})
#
