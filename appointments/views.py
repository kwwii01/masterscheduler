from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Appointment, Service
from .forms import AppointmentForm


# @login_required('appointment:index')
def create_appointment(request):
    form = AppointmentForm()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            master = form.cleaned_data['master']
            appointment_date = form.cleaned_data['appointment_date']
            client = request.user
            status = 'PLD'
            new_appointment = Appointment(service=service, master=master, appointment_date=appointment_date,
                                          client=client, status=status)
            new_appointment.save()
            return redirect('home:index')
    return render(request, 'appointments/create_appointment.html', {'form': form})


def load_masters(request):
    service_id = request.GET.get('service_id')
    chosen_service = Service.objects.get(pk=service_id)
    masters = chosen_service.masters.all()
    return render(request, 'appointments/masters_dropdown_list_options.html', {'masters': masters})

