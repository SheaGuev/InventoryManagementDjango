from django import forms
from .models import Device, DeviceConfig

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name', 'device_type', 'device_desc', 'device_status', 'return_day']

class NewDeviceForm(forms.ModelForm):
    device_serial = forms.CharField(max_length=255)

    class Meta:
        model = Device
        fields = ['device_name', 'device_type', 'device_desc', 'device_status', 'location', 'return_day']

    def save(self, commit=True):
        device = super(NewDeviceForm, self).save(commit=False)
        device_serial = self.cleaned_data.get('device_serial')

        # Create a new DeviceConfig object
        config = DeviceConfig.objects.create(device_serial=device_serial)
        device.config = config

        if commit:
            device.save()
        return device