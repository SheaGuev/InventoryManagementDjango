from django.contrib import admin
from .models import Location, Device, DeviceConfig, Role, CustomUser, Booking
# Register your models here.
# Register your models here.
admin.site.register(Location)
admin.site.register(Device)
admin.site.register(DeviceConfig)
admin.site.register(Role)  # Register the Role model
admin.site.register(CustomUser)
admin.site.register(Booking)