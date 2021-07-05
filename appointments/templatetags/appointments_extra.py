import datetime
from django import template
import datetime

register = template.Library()


@register.simple_tag
def get_time_list(schedule_dict, key):
    formatted_schedule_list = []
    for time in schedule_dict[key]:
        formatted_schedule_list.append(time.strftime('%H:%M'))
    return formatted_schedule_list
