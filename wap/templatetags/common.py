import json

from django import template
from datetime import datetime, timedelta

from django.template.defaultfilters import safe
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

from wap.constances import DAY_NAME, VERSION_NAME
register = template.Library()

@register.filter
def get_day_in_week(date):
    if not isinstance(date, datetime):
        date = string_to_datetime(date)
    if date:
        if date.date() == datetime.today().date():
            return "Hôm nay"
        return DAY_NAME[date.weekday()]
    return ""

@register.filter
def get_date_in_month(date):
    if not isinstance(date, datetime):
        date = string_to_datetime(date)
    if date:
        return date.day
    return ""

@register.filter
def string_to_datetime(string, date_format="%d/%m/%Y %H:%M:%S"):
    try:
        date = datetime.strptime(string, date_format)
        return date
    except:
        return ""

@register.filter
def get_session_by_date(sessions, date):
    if not isinstance(date, datetime):
        date = string_to_datetime(date)
    if date:
        return sessions.get(date.strftime("%d%m%Y"))
    return None

@register.filter
def get_session_time(session):
    if session and 'sessionTime' in session and session['sessionTime']:
        date = string_to_datetime(session['sessionTime'])
        if date:
            return date.strftime('%H:%M')
    return ""

@register.filter
def film_duration(minutes, is_minute=False):
    duration = 'Đang cập nhật'
    if minutes:
        if is_minute:
            return str(minutes) + " phút"
        duration = ''
        parsed = str(timedelta(minutes=minutes))[:-3].split(":")
        if int(parsed[0]) > 0:
            duration += parsed[0] + " giờ "
        if int(parsed[1]) > 0:
            duration += parsed[1] + " phút"
    return duration


@register.filter
def film_time(session_time, duration):
    time = ''
    if session_time:
        date = string_to_datetime(session_time)
        if date:
            time = date.strftime('%I:%M%p').lstrip('0').lower()
            if duration:
                end_time = date + timedelta(minutes=duration)
                if end_time:
                    time += ' ~ ' + end_time.strftime('%I:%M%p').lstrip('0').lower()
                else:
                    time += ' ~ Đang cập nhật'
            else:
                time += ' ~ Đang cập nhật'
        else:
            time = 'Đang cập nhật'
    return time

@register.filter
def get_items(dict):
    return dict.items()

@register.filter
def get_dict_value(dict, key):
    return dict.get(key)

@register.filter
def get_list_value(list, index):
    return list[index]

@register.filter
def get_version_name(version_id):
    return VERSION_NAME.get(version_id, 'Đang cập nhật')

@register.filter
def booked_seat(seats):
    return mark_safe('<span class="clrgrey"> | </span>'.join('<span class="label-main"><b>' + seat.strip() + '</b></span>' for seat in seats.split(',')))

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""

@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])

@register.simple_tag
def define(val=None):
  return val

@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')

@register.filter
def to_json_string(value):
    return mark_safe(json.dumps(value))

@register.filter
def imdb(value):
    return "%.1f" % value