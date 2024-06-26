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
from datetime import timedelta


####SHEAS CODE FOR BOOKINGS
@require_POST
@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.booking_status = "reserved"
    booking.save()
    ##create notification for user and admin
    UserNotification.createNew(booking.user, "Your booking has been approved.")
    admin_users = CustomUser.objects.filter(role__role_name='admin')
    for admin in admin_users:
        UserNotification.createNew(admin, f"Booking {booking_id} has been approved.")
    return redirect('reservations')

@require_POST
@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    ##create notification for user and admin
    UserNotification.createNew(booking.user, "Your booking has been rejected.")
    admin_users = CustomUser.objects.filter(role__role_name='admin')
    for admin in admin_users:
        UserNotification.createNew(admin, f"Booking {booking_id} has been rejected.")
    return redirect('reservations')


##Shea's code for booking a device
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
        UserNotification.createNew(booking.user, "Your booking request has been submitted.")
        admin_users = CustomUser.objects.filter(role__role_name='admin')
        for admin in admin_users:
            UserNotification.createNew(admin, f"New booking request {booking.id} has been submitted.")
        return redirect('device_view', device_serial=device.config.device_serial)
    else:
        messages.error(request, 'This device is not available for reservation.')  # Display an error message
        return redirect('device_view', device_serial=device.config.device_serial)
    # Update device status
#Shea's code for cancelling a reservation
@login_required
def cancel_reservation(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    booking = get_object_or_404(Booking, device=device, user=request.user)

    booking.delete()
    # Update device status
    # Update device status
    booking.device.update_device_status()
    return redirect('device_view', device_serial=device.config.device_serial)

#SHEA'S CODE FOR EQUIPMENT PAGES
@login_required
def equipment(request):
    devices, search = _search(request)
    user = request.user
    context = {
        "devices": devices,
        "search": search or "",
        "user": user,
    }
    return render(request, 'equipmentSearch.html', context)
#Shea's code for search functionality
@login_required
def search_view(request):
    devices, search = _search(request)
    context = {
        "devices": devices,
        "search": search or "",
        'current_path': request.path,
    }
    return render(request, 'search.html', context)
##DEVICE PAGE BELOW Shea
@login_required
def device_view(request, device_serial):
    device = Device.objects.get(config__device_serial=device_serial)
    form = DeviceForm(instance=device)
    booking = Booking.objects.filter(device=device, user=request.user).first()
    user=request.user
    return render(request, 'device.html', {'device': device, 'form': form, 'booking': booking, "user": user})
#Shea's code for search functionality
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
        if device_status is not None:
            if device_status.lower() == 'true':
                devices = devices.filter(device_status=True)
            elif device_status.lower() == 'false':
                devices = devices.filter(device_status=False)
        if device_type:
            devices = devices.filter(device_type__icontains=device_type)

        paginator = Paginator(devices, 4)

        page = paginator.get_page(page_number)

        return page, search or ""

##Shea's code for device edit
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
#Shea's code for deleting a device
@login_required
def delete_device(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    device.delete()
    return redirect('equipment')  # Redirect to the equipment page

#Shea's code for deleting a booking
@login_required
@require_POST
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    device = booking.device
    booking.delete()
    device.device_status = True  # Set the device status to available
    device.save()
    return redirect('reservations')  # Redirect to the reservations page

#SHEA'S and Harsh's code for deleting a notification
@require_POST
@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(UserNotification, id=notification_id)
    notification.delete()
    return redirect('notifications')  # Redirect to the notifications page
#Shea's device view
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
#MICAH'S CODE FOR EQUIPMENT REQUEST PAGES
@login_required
def equipmentRequests(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "equipmentRequest.html", { "bookings": bookings })

#MICAH'S CODE FOR EQUIPMENT REQUEST PAGES
@login_required
def reservations(request):
    bookings = Booking.objects.filter(booking_status="requested")
    all_bookings = Booking.objects.all()
    all_bookings = all_bookings.exclude(booking_status="requested")
    return render(request, "reservations.html", { "bookings": bookings, "all_bookings": all_bookings });


#MICAH'S CODE FOR NOTIFICATIONS
@login_required
def notifications(request):
    notifications = UserNotification.objects.filter(user=request.user).order_by('-created')
    return render(request, 'notifications.html', {'notifications': notifications})
#Micah's device group for reports page
class DeviceGroup(object):
    def __init__(self, name, devices, total):
        self.name = name
        self.devices = devices
        self.total = total

    devices = {}
    total = 0
    name = ""
#Micah's, Jamal's code for reports page
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

#logout micah
def logoutUser(request):
    logout(request)



# Harsh's views for registration, aithenticaion and login connected parts can be found in authenticaion app
@login_required
def user_home(request):
    users = CustomUser.objects.all()
    bookings = Booking.objects.filter(booking_status="requested")

    try:
        notifications = UserNotification.objects.filter(user=request.user).order_by("-created")
    except:
        notifications = list()

    user = request.user
    devices, search = _search(request)
    latest_booking = Booking.objects.filter(user=request.user).order_by('-booking_req_date').first()
    context = {
        "devices": devices,
        "search": search or "",
        'users': users,
        'bookings': bookings,
        "notifications": notifications,
        "user": user,
        "latest_booking": latest_booking

    }
    return render(request, 'user_home.html', context)

@login_required
def admin_home(request):
    devices, search = _search(request)
    users = CustomUser.objects.all()
    bookings = Booking.objects.filter(booking_status="requested")
    user = request.user

    try:
        notifications = UserNotification.objects.filter(user=request.user).order_by("-created")
    except:
        notifications = list()

    context = {
        "devices": devices,
        "search": search or "",
        'users': users,
        'bookings': bookings,
        "notifications": notifications,
        "user": user

    }

    #print(context)
    return render(request, 'admin_home.html', context)

logger = logging.getLogger(__name__)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')  # Set username to be the same as email
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Email already exists. Please choose a different email.")

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
