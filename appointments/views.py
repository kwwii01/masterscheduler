from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
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


@login_required
def index(request):
    appointments = request.user.appointments_as_client.all()
    return render(request, 'appointments/index.html', {'appointments': appointments})


@login_required
def filtered_by_status(request, appointment_status):
    appointments = Appointment.objects.filter(status=appointment_status)
    return render(request, 'appointments/index.html', {'appointments': appointments})


@login_required
def details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.user != appointment.client and request.user != appointment.master.user:
        messages.error(request, "You're not participating in this event.")
        return redirect('appointments:index')
    return render(request, 'appointments/details.html', {'appointment': appointment})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.user != appointment.client and request.user != appointment.master.user:
        messages.error(request, "You're not permitted to do this.")
        return redirect('appointments:index')
    appointment.status = 'CLD'
    appointment.save()
    return redirect('appointments:details', appointment_id=appointment_id)


@login_required
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
            if request.user == master.user:
                messages.warning(request, "You can't be master and client at the same time.")
                return redirect('appointments:create')
            client = request.user
            status = 'PLD'
            new_appointment = Appointment(service=service, master=master, appointment_date=appointment_date,
                                          client=client, status=status)
            new_appointment.save()
            messages.success(request, 'Appointment successfully created!')
            return redirect('appointments:index')
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
