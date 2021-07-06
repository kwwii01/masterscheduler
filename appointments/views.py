from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

from .models import Appointment, Service, Master, convert_to_verbal_dict, WorkDay, WorkTime
from .forms import AppointmentForm


def convert_day_format(day):
    if day == 6:
        return 0
    else:
        return day + 1


def get_master_or_none(user):
    try:
        current_master = user.master
        return current_master
    except Master.DoesNotExist:
        return None



@login_required
def index(request):
    appointments = request.user.appointments_as_client.all()
    return render(request, 'appointments/index.html', {'appointments': appointments})


@login_required
def index_as_master(request):
    current_master = get_master_or_none(request.user)
    if current_master is None:
        messages.error(request, "You're not master")
        return redirect('appointments:index')
    appointments = request.user.master.appointments_as_master.all()
    return render(request, 'appointments/index.html', {'appointments': appointments})


@login_required
def filtered_by_status(request, appointment_status):
    appointments = request.user.appointments_as_client.filter(status=appointment_status)
    return render(request, 'appointments/index.html', {'appointments': appointments})


@login_required
def details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.user != appointment.client and request.user != appointment.master.user:
        messages.error(request, "You're not participating in this event.")
        return redirect('appointments:index')
    return render(request, 'appointments/details.html', {'appointment': appointment})


def masters(request):
    masters_list = Master.objects.all()
    return render(request, 'appointments/masters.html', {'masters': masters_list})


@login_required
def master_view(request, master_id):
    master = get_object_or_404(Master, pk=master_id)
    schedule_dict = convert_to_verbal_dict(master.generate_dict())
    return render(request, 'appointments/master.html', {'master': master, 'schedule_dict': schedule_dict})


@login_required
def master_edit(request, master_id):
    master = get_object_or_404(Master, pk=master_id)
    current_master = get_master_or_none(request.user)
    if current_master is None:
        messages.error(request, "You're not permitted to do this.")
        return redirect('appointments:masters')
    if current_master == master:
        if request.method == 'POST':
            master.service_set.clear()
            master.work_days.clear()
            services = request.POST.getlist('services')
            workdays = request.POST.getlist('schedule')
            for service in services:
                master.service_set.add(Service.objects.get(pk=service))
            for workday in workdays:
                master.work_days.add(WorkDay.objects.get(pk=workday))
            return redirect('appointments:master_view', master_id=master.id)
        else:
            services = Service.objects.all()
            created_workdays = WorkDay.objects.all()
            return render(request, 'appointments/master_edit.html',
                          {'services': services, 'master': master, 'created_workdays': created_workdays})
    else:
        messages.error(request, "You're not permitted to do this.")
        return redirect('appointments:masters')


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


@login_required
def add_workday(request):
    current_master = get_master_or_none(request.user)
    if current_master is None:
        messages.error(request, "You're not permitted to do this.")
        return redirect('appointments:masters')
    weekday = request.GET.get('weekday')
    time = request.GET.get('time')
    new_workday = WorkDay(weekday=weekday)
    new_worktime = WorkTime(time=time)
    new_worktime.save()
    new_workday.save()
    new_workday.worktimes.add(new_worktime)
    workdays = WorkDay.objects.all()
    return render(request, 'appointments/workday_select_options.html', {'workdays': workdays, 'master': current_master})

