from django import template
from datetime import datetime

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
def get_dict_value(dict, key):
    return dict.get(key)

@register.filter
def get_list_value(list, index):
    return list[index]

@register.filter
def get_version_name(version_id):
    return VERSION_NAME.get(version_id)

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