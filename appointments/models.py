from django.db import models
from django.contrib.auth.models import User


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Service(models.Model):
    service_type = models.CharField(
        max_length=60,
        unique=True,
    )
    masters = models.ManyToManyField(Master)

    def __str__(self):
        return self.service_type


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_client')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments_as_master')
    CANCELED = 'CLD'
    PENDING = 'PDG'
    COMPLETED = 'CPD'
    PLANNED = 'PLD'
    STATUS_CHOICES = [
        (CANCELED, 'Appointment is canceled'),
        (PENDING, 'Appointment is in progress'),
        (COMPLETED, 'Appointment is completed'),
        (PLANNED, 'Appointment is planned'),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=PLANNED,
    )

    def __str__(self):
        return self.service.__str__()

