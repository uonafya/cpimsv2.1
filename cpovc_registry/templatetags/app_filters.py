from django import template
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from cpovc_main.functions import get_dict
from cpovc_registry.models import AppUser

register = template.Library()

# Declare Constants For Lookups
check_fields = ['intervention_id',
                'case_category_id',
                'core_item_id']
vals = get_dict(field_name=check_fields)


@register.filter(name='gen_value')
def gen_value(value, args):
    if value in args:
        return args[value]
    else:
        return value


@register.filter(name='gen_username')
def gen_username(value):
    username = None
    if value:
        app_users = AppUser.objects.filter(id=value)
        for app_user in app_users:
            username = app_user.username
        return username.capitalize()
    else:
        return value


@register.filter(name='gen_age')
def gen_age(value):
    now = timezone.now()
    date_today = None
    date_of_birth = None
    if value:
        date_today = now.date()
        date_of_birth = value
        age = relativedelta(date_today, date_of_birth).years
        # print 'date_today: %s  | date_of_birth: %s | diff in yrs: %s'
        # %(date_today, date_of_birth, age)
        return age
    else:
        return 0


@register.filter(name='gen_value2')
def gen_value2(value):
    if value:
        value = str(gen_value(value, vals))
        return value
    else:
        return value


@register.filter(name='gen_refferal', is_safe=True)
def gen_refferal(value):
    value_list = []
    values = None
    value = value[0]
    if type(value) is dict:
        values = value['ovcrefs']
        for val in values:
            value_list.append(str(gen_value(val.refferal_to, vals)))
    # Generate HtmlMarkUp
    mark_up = ''
    for v in value_list:
        mark_up += '%s<br>' %v
    return mark_up


@register.filter(name='gen_intervention')
def gen_intervention(value):
    value_list = []
    values = None
    value = value[0]
    if type(value) is dict:
        values = value['ovcintvs']
        for val in values:
            value_list.append(str(gen_value(val.intervention, vals)))
    # Generate HtmlMarkUp
    mark_up = ''
    for v in value_list:
        mark_up += '%s<br>' %v
    return mark_up


@register.filter(name='gen_date_of_event')
def gen_date_of_event(value):
    value = value[0]
    if type(value) is dict:
        values = value['date_of_event']
    return values

@register.filter(name='gen_case_grouping_id')
def gen_case_grouping_id(value):
    value = value[0]
    values= None
    if type(value) is dict:
        values = value['case_grouping_id']
    return values
