from django.shortcuts import render, HttpResponse
from . models import Device, DeviceConfig

# Create your views here.
def home(request):
    devicesall = Device.objects.all()
    return render(request, 'equipmentSearch.html', {"devices": devicesall})


def search(request):
    pass
    # if request.method == 'POST':
    #     search_text = request.POST['search_text']
    # else:
    #     search_text = ''
    #
    # devices = Device.objects.filter(device_name__contains=search_text)
    # return render(request, 'ajax_search.html', {'devices': devices})

def reservations(request):
    
    return render(request, "reservations.html");