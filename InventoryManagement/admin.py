from django.contrib import admin
from .models import Location, Device, DeviceConfig, Role, User, Booking
# Register your models here.
# Register your models here.
admin.site.register(Location)
admin.site.register(Device)
admin.site.register(DeviceConfig)
admin.site.register(Role)  # Register the Role model
admin.site.register(User)
admin.site.register(Booking)