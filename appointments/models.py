from django.db import models
from django.contrib.auth.models import User


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


def convert_to_verbal(weekday_id):
    for weekday_choice in WEEKDAY_CHOICES:
        if weekday_choice[0] == weekday_id:
            return weekday_choice[1]


def convert_to_verbal_dict(simple_dict):
    verbal_dict = {}
    for key in simple_dict.keys():
        verbal_dict[convert_to_verbal(key)] = simple_dict[key]
    return verbal_dict


class WorkTime(models.Model):
    time = models.TimeField(unique=True)

    def __str__(self):
        return self.time.strftime('%H:%M')


class WorkDay(models.Model):
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
    )
    worktimes = models.ManyToManyField(WorkTime)

    def __str__(self):
        times_str = ''
        worktimes_list = self.worktimes.all()
        for i, worktime in enumerate(worktimes_list):
            times_str = times_str + worktime.__str__()
            if i != worktimes_list.count() - 1:
                times_str = times_str + ', '
        return convert_to_verbal(self.weekday) + ' - ' + times_str


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_days = models.ManyToManyField(WorkDay, null=True)

    def generate_dict(self):
        weekday_times_dict = {}
        for work_day in self.work_days.all():
            if work_day.weekday not in weekday_times_dict.keys():
                worktimes = []
                for worktime in work_day.worktimes.all():
                    worktimes.append(worktime.time)
                worktimes.sort()
                weekday_times_dict[work_day.weekday] = worktimes
            else:
                worktimes = weekday_times_dict[work_day.weekday]
                for worktime in work_day.worktimes.all():
                    if worktime not in worktimes:
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
    masters = models.ManyToManyField(Master, null=True)

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

