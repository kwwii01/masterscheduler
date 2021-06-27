from django.contrib import admin

from .models import Master, Service, Appointment, WorkDay, WorkTime

# Register your models here.
admin.site.register(Master)
admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(WorkDay)
admin.site.register(WorkTime)
