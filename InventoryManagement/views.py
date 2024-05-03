from datetime import date

from django.http import HttpRequest, request
from django.shortcuts import render, HttpResponse

from authentication.forms import NewUserForm, LoginForm
from .models import Booking, Device, DeviceConfig, Role, UserNotification
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from . models import Device, DeviceConfig
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import DeviceForm, NewDeviceForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import logging
from InventoryManagement.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user
from django.views.decorators.http import require_POST


# @login_required
# def admin_home(request):
#     users = CustomUser.objects.all()
#     return render(request, 'admin_home.html', {'users': users})


# @login_required
# def home(request):
#     # context = {
#     #     "user": CustomUser,
#     # }
#     return render(request, 'index.html')

@require_POST
@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.booking_status = "reserved"
    booking.save()
    return redirect('reservations')

@require_POST
@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('reservations')
@login_required
def equipment(request):
    devices, search = _search(request)
    context = {
        "devices": devices,
        "search": search or "",
    }
    return render(request, 'equipmentSearch.html', context)

@login_required
def search_view(request):
    devices, search = _search(request)
    context = {
        "devices": devices,
        "search": search or "",
        'current_path': request.path,
    }
    return render(request, 'search.html', context)

@login_required
def device_view(request, device_serial):
    device = Device.objects.get(config__device_serial=device_serial)
    form = DeviceForm(instance=device)
    booking = Booking.objects.filter(device=device, user=request.user).first()
    return render(request, 'device.html', {'device': device, 'form': form, 'booking': booking})
@login_required
def _search(request):
        search = request.GET.get('search')
        return_date_gt = request.GET.get('return_day>')
        return_date_lt = request.GET.get('return_day<')
        device_status = request.GET.get('device_satus')
        device_type = request.GET.get('device_type')
        page_number = request.GET.get('page', 1)  # default to page 1 if not provided

        devices = Device.objects.all()

        if search:
            devices = devices.filter(device_name__icontains=search)
        if return_date_gt:
            devices = devices.filter(return_day__gte=return_date_gt)
        if return_date_lt:
            devices = devices.filter(return_day__lte=return_date_lt)
        # if return_date_gt and return_date_lt:
        #     devices = devices.filter(Q(return_day__gte=return_date_gt) & Q(return_day__lte=return_date_lt))
        # if return_date:
        #     devices = devices.filter(return_date__icontains=return_date)
        # if pickup_date:
        #     devices = devices.filter(pickup_date__icontains=pickup_date)
        if device_status:
            devices = devices.filter(device_status__icontains=device_status)
        if device_type:
            devices = devices.filter(device_type__icontains=device_type)

        paginator = Paginator(devices, 4)

        page = paginator.get_page(page_number)

        return page, search or ""

from datetime import timedelta

@login_required
def reserve_device(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    if device.device_status:  # Check if the device status is true
        booking = Booking(device=device, user=request.user)
        booking.booking_status = "requested"
        booking.booking_req_date = date.today()
        booking.device_exp_ret_date = date.today() + timedelta(days=device.return_day)  # Set expected return date to a week from today
        booking.save()
        booking.device.update_device_status()
        return redirect('device_view', device_serial=device.config.device_serial)
    else:
        messages.error(request, 'This device is not available for reservation.')  # Display an error message
        return redirect('device_view', device_serial=device.config.device_serial)
    # Update device status

@login_required
def cancel_reservation(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    booking = get_object_or_404(Booking, device=device, user=request.user)

    booking.delete()
    # Update device status
    # Update device status
    booking.device.update_device_status()
    return redirect('device_view', device_serial=device.config.device_serial)


# @login_required
# def reserve_device(self, user, device_serial):
#     if '/device/' in request.GET:
#         device = get_object_or_404(Device, config__device_serial=device_serial)
#     booking = self.objects.model(device, user)
#     booking.booking_status = "reserved"
#     booking.booking_req_date = date.today()
#
#     booking.save()
#     return

    # if request.method == 'POST':
    #     search_text = request.POST['search_text']
    # else:
    #     search_text = ''
    #
    # devices = Device.objects.filter(device_name__contains=search_text)
    # return render(request, 'ajax_search.html', {'devices': devices})

@login_required
def equipmentRequests(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "equipmentRequest.html", { "bookings": bookings })

@login_required
def reservations(request):
    bookings = Booking.objects.filter(booking_status="requested")
    all_bookings = Booking.objects.all()
    all_bookings = all_bookings.exclude(booking_status="requested")
    return render(request, "reservations.html", { "bookings": bookings, "all_bookings": all_bookings });

@login_required
def edit_device(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save()
            return redirect('device_view', device_serial=device.config.device_serial)
        else:
            print(form.errors)  # Print form errors
    else:
        form = DeviceForm(instance=device)
    return render(request, 'device.html', {'form': form, 'device': device})

@login_required
def delete_device(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    device.delete()
    return redirect('equipment')  # Redirect to the equipment page
@login_required
@require_POST
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('reservations')  # Redirect to the reservations page

@login_required
def notifications(request):
    notifications = UserNotification.objects.filter(user=request.user).order_by('-created')
    return render(request, 'notifications.html', {'notifications': notifications})

@require_POST
@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(UserNotification, id=notification_id)
    notification.delete()
    return redirect('notifications')  # Redirect to the notifications page
# DELETE DUPLICATED FROM DB SCRIPT: PREVENT NOT NULL ERROR
# from django.db.models import Count
# from InventoryManagement.models import DeviceConfig
#
# # Find duplicate device_serial values
# duplicates = (DeviceConfig.objects.values('device_serial')
#               .annotate(device_serial_count=Count('device_serial'))
#               .filter(device_serial_count__gt=1))
#
# for duplicate in duplicates:
#     # Get all DeviceConfig objects with this device_serial
#     configs = DeviceConfig.objects.filter(device_serial=duplicate['device_serial'])
#
#     for config in configs[1:]:
#         config.delete()

@login_required
def add_device(request):
    if request.method == 'POST':
        form = NewDeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment')
    else:
        form = NewDeviceForm()
    return render(request, 'add_device.html', {'form': form})

class DeviceGroup(object):
    def __init__(self, name, devices, total):
        self.name = name
        self.devices = devices
        self.total = total

    devices = {}
    total = 0
    name = ""

def reports(request):
    deviceTypes = Device.objects.all().values_list("device_type", flat=True).distinct()
    deviceGroups = {}

    for type in deviceTypes:
        devices = Device.objects.filter(device_type=type)
        total = 0
        name = str(type)

        for device in devices:
            total += 1

        deviceGroups[type] = DeviceGroup(name, devices, total)

    print(deviceGroups)
    return render(request, "reports.html", { "groups": deviceGroups })

def logoutUser(request):
    logout(request)



# Harsh's views
@login_required
def user_home(request):
    try:
        notifications = UserNotification.objects.order_by("-created")
    except:
        notifications = list()

    devices, search = _search(request)
    latest_booking = Booking.objects.filter(user=request.user).order_by('-booking_req_date').first()
    context = {
        "devices": devices,
        "search": search or "",
        "latest_booking": latest_booking,
    }
    return render(request, 'user_home.html', context)

@login_required
def admin_home(request):
    devices, search = _search(request)
    users = CustomUser.objects.all()
    bookings = Booking.objects.filter(booking_status="requested")


    try:
        notifications = list(UserNotification.objects.order_by("-created"))
    except:
        notifications = list()

    context = {
        "devices": devices,
        "search": search or "",
        'users': users,
        'bookings': bookings,
        "notifications": notifications
    }

    #print(context)
    return render(request, 'admin_home.html', context)



logger = logging.getLogger(__name__)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                logger.info('User registered successfully. Email: %s', user.email)
                messages.success(request, "Registration successful.")
                return redirect("login")  # Redirect to the login page
            except Exception as e:
                logger.error('Error during user creation: %s', str(e))
                messages.error(request, "Unsuccessful registration. Error during user creation.")
        else:
            logger.warning('Unsuccessful registration. Form errors: %s', form.errors)
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                logger.info('User authenticated, redirecting to placeholder page.')
                if user.role.role_name == 'admin':
                    return redirect("admin_home")  # Redirect to the admin home page
                else:
                    return redirect("user_home")  # Redirect to the user home page
            else:
                logger.warning('Invalid email or password. Email: %s', email)
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def custom_logout(request):
    print(request.user.id)
    logout(request)

    return redirect('login')


class UserForm:
    pass


def placeholder(request):
    return render(request, 'placeholder.html')


def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'list_users.html', {'users': users})


@require_POST
def make_admin(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    admin_role = Role.objects.get(role_name='admin')  # Retrieve the 'admin' role
    user.role = admin_role  # Assign the 'admin' role to the user
    user.save()
    return redirect('admin_home')

@require_POST
def make_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user_role = Role.objects.get(role_name='user')  # Retrieve the 'user' role
    user.role = user_role  # Assign the 'admin' role to the user
    user.save()
    return redirect('admin_home')

@require_POST
def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect('admin_home')

