from django.db import models
from django.contrib.auth.models import User


class WorkTime(models.Model):
    time = models.TimeField(unique=True)

    def __str__(self):
        return str(self.time)


class WorkDay(models.Model):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 0
    WEEKDAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
    )
    worktimes = models.ManyToManyField(WorkTime)

    def __str__(self):
        for weekday_choice in self.WEEKDAY_CHOICES:
            if weekday_choice[0] == self.weekday:
                return weekday_choice[1]


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_days = models.ManyToManyField(WorkDay)

    def generate_dict(self):
        weekday_times_dict = {}
        for work_day in self.work_days.all():
            if work_day.weekday not in weekday_times_dict.keys():
                worktimes = []
                for worktime in work_day.worktimes.all():
                    worktimes.append(worktime.time)
                worktimes.sort()
                weekday_times_dict[work_day.weekday] = worktimes
        return weekday_times_dict

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

    def get_status_verbal_name(self):
        for pair in self.STATUS_CHOICES:
            if pair[0] == self.status:
                return pair[1]

    def __str__(self):
        return self.service.__str__() + ' ' + str(self.appointment_date) + ' ' + self.master.user.username

