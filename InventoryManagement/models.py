from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.device_name


class DeviceConfig(models.Model):
    device_serial = models.CharField(max_length=50, unique=True, null=False)
    device_cpu = models.CharField(max_length=50, null=True, blank=True)
    device_gpu = models.CharField(max_length=50, null=True, blank=True)
    device_ram = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.device_serial


class Role(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    role_desc = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.role_name


class User(models.Model):

    def get_default_role():
        return Role.objects.get(role_name='user').pk

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    approval_status = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=get_default_role)
    user_fname = models.CharField(max_length=50)
    user_sname = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user_fname} {self.user_sname}"


class Booking(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_req_date = models.DateField()
    booking_status = models.CharField(max_length=50)
    status_change_date = models.DateTimeField(auto_now_add=True)
    collected_status = models.BooleanField(default=False)
    collected_date = models.DateTimeField(null=True, blank=True)
    device_exp_ret_date = models.DateField()
    device_act_ret_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.device}"



