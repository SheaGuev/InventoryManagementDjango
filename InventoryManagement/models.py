from datetime import date
from multiprocessing.managers import BaseManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager

# User = get_user_model()
# user = User.objects.first()  # get an instance of User, which is actually CustomUser
# default_role = user.get_default_role()
# from authentication import models


class Location(models.Model):
    location_name = models.CharField(max_length=128)
    location_desc = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.location_name


class Device(models.Model):
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    device_desc = models.CharField(max_length=200, null=True, blank=True)
    device_status = models.BooleanField(default=False)  # Changed from CharField to BooleanField
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    config = models.ForeignKey('DeviceConfig', on_delete=models.CASCADE, null=False, blank=False)
    return_day = models.IntegerField(default=0)
    # device_count = models.IntegerField(default=0)

    def __str__(self):
        return self.device_name


class DeviceConfig(models.Model):
    device_serial = models.CharField(max_length=50, unique=True, null=False)
    device_cpu = models.CharField(max_length=50, null=True, blank=True)
    device_gpu = models.CharField(max_length=50, null=True, blank=True)
    device_ram = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.device_serial


# class Role(models.Model):
#     ROLE_CHOICES = (
#         ('user', 'User'),
#         ('admin', 'Admin'),
#     )
#     role_name = models.CharField(max_length=50, choices=ROLE_CHOICES)
#     role_desc = models.CharField(max_length=200, null=True, blank=True)
#
#     def __str__(self):
#         return self.role_name


# class User(models.Model):
#
#     def get_default_role(self):
#         return Role.objects.get(role_name='user').pk
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     approval_status = models.BooleanField(default=False)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, default=get_default_role)
#     user_fname = models.CharField(max_length=50)
#     user_sname = models.CharField(max_length=50)
#     user_email = models.EmailField()
#     user_phone = models.CharField(max_length=20)

    # def __str__(self):
    #     return f"{self.user_fname} {self.user_sname}"


    # def __str__(self):
    #     return self.role_name

# def get_user_role():
#     return Role.objects.get_or_create(role_name='user')[0].id
#
# class CustomUser(AbstractUser):
#     username = models.CharField(max_length=255, unique=False, blank=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20)
#     role = models.ForeignKey(Role, on_delete=models.SET(get_user_role), default=get_user_role)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


class Role(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    role_desc = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.role_name

# def get_user_role():
#     return Role.objects.get_or_create(role_name='user')[0].id

# class CustomUser(AbstractUser):
#     username = models.CharField(max_length=255, unique=False, blank=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20)
#     role = models.ForeignKey(Role, on_delete=models.SET('user'), default='user')
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

    # def get_default_role(self):
    #     return Role.objects.get_or_create(role_name='user')[0].id



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)
def get_user_role():
    try: 
        return Role.objects.get_or_create(role_name='user')[0].id
    except: 
        return 3

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.ForeignKey(Role, on_delete=models.SET(get_user_role), default=get_user_role)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class UserNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message =  models.CharField(max_length=65535)
    created = models.DateTimeField(auto_now_add=True)

    def createNew(user, message):
        notification = UserNotification()
        notification.user = user
        notification.message = message

        notification.save()
    
    def __str__(self):
        return f"{self.message}"
        

class Booking(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_req_date = models.DateField()
    booking_status = models.CharField(max_length=50)
    status_change_date = models.DateTimeField(auto_now_add=True)
    collected_status = models.BooleanField(default=False)
    collected_date = models.DateTimeField(null=True, blank=True)
    device_exp_ret_date = models.DateField()
    device_act_ret_date = models.DateField(null=True, blank=True)

    def reserve_device(deviceId, user):
        booking = Booking()
        booking.deviceId = deviceId
        booking.user = user
        booking.booking_status = "reserved"
        booking.booking_req_date = date.today()

        booking.save()
        return
    
    def cancel_reservation(self, bookingId, userId):
        booking = self.objects.get(pk=bookingId,user__id=userId)
        if booking:
            booking.booking_status = "cancelled"
            booking.save()

    def __str__(self):
        return f"{self.user} - {self.device}"