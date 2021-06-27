from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, Service, Master
from .forms import AppointmentForm


def convert_day_format(day):
    if day == 6:
        return 0
    else:
        return day + 1


# @login_required('appointment:index')
def create_appointment(request):
    form = AppointmentForm()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            master = form.cleaned_data['master']
            appointment_date = form.cleaned_data['appointment_date']
            master_datetime_dict = master.generate_dict()
            converted_day = convert_day_format(appointment_date.weekday())
            if converted_day not in master_datetime_dict.keys():
                messages.warning(request, 'Selected weekday is not available for chosen master.')
                return redirect('appointments:create')
            if appointment_date.time() not in master_datetime_dict[converted_day]:
                messages.warning(request, 'Selected time is not available for chosen master.')
                return redirect('appointments:create')
            if appointment_date < timezone.now():
                messages.warning(request, "Appointment can't be in the past, try another date and time.")
                return redirect('appointments:create')
            client = request.user
            status = 'PLD'
            new_appointment = Appointment(service=service, master=master, appointment_date=appointment_date,
                                          client=client, status=status)
            new_appointment.save()
            messages.success(request, 'Appointment successfully created!')
            return redirect('home:index')
    return render(request, 'appointments/create_appointment.html', {'form': form})


def load_masters(request):
    service_id = request.GET.get('service_id')
    chosen_service = Service.objects.get(pk=service_id)
    masters = chosen_service.masters.all()
    return render(request, 'appointments/masters_dropdown_list_options.html', {'masters': masters})


def load_workschedule(request):
    master_id = request.GET.get('master_id')
    chosen_master = Master.objects.get(pk=master_id)
    return JsonResponse(chosen_master.generate_dict())

