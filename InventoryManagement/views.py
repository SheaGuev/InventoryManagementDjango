from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from . models import Device, DeviceConfig
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import DeviceForm


def home(request):
    return render(request, 'index.html')

# Create your views here.
def equipment(request):
    devices, search = _search(request)
    context = {
        "devices": devices,
        "search": search or "",
    }
    return render(request, 'equipmentSearch.html', context)

def search_view(request):
    devices, search = _search(request)
    context = {
        "devices": devices,
        "search": search or "",
    }
    return render(request, 'search.html', context)

def device_view(request, device_serial):
    device = Device.objects.get(config__device_serial=device_serial)
    form = DeviceForm(instance=device)
    return render(request, 'device.html', {'device': device, 'form': form})
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


    # if request.method == 'POST':
    #     search_text = request.POST['search_text']
    # else:
    #     search_text = ''
    #
    # devices = Device.objects.filter(device_name__contains=search_text)
    # return render(request, 'ajax_search.html', {'devices': devices})

def edit_device(request, device_serial):
    device = get_object_or_404(Device, config__device_serial=device_serial)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save()
            return redirect('view_device', device_serial=device.config.device_serial)
    else:
        form = DeviceForm(instance=device)
    return render(request, 'device.html', {'form': form, 'device':device})

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