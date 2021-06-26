from django.forms import ModelForm, HiddenInput

from .models import Appointment, Service


class AppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields = ['service', 'master', 'appointment_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Service.objects.none()
        self.fields['appointment_date'].input_formats = ['%d/%m/%Y %H:%M']

        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                chosen_service = Service.objects.get(pk=service_id)
                self.fields['master'].queryset = chosen_service.masters.all()
            except (ValueError, TypeError):
                pass


