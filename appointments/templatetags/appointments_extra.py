import datetime
from django import template
from django.contrib.auth.models import User
from ..models import Master

register = template.Library()


@register.simple_tag
def get_time_list(schedule_dict, key):
    formatted_schedule_list = []
    for time in schedule_dict[key]:
        formatted_schedule_list.append(time.strftime('%H:%M'))
    return formatted_schedule_list


@register.simple_tag
def authorize_master(current_user):
    try:
        current_master = current_user.master
        return True
    except Master.DoesNotExist:
        return False
