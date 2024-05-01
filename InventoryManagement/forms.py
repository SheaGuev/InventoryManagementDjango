from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name', 'device_type', 'device_desc', 'device_status', 'location', 'config', 'return_day']
