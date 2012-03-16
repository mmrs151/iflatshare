from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='environment_name')
def get_environment(environment):
    return settings.ENV

@register.filter(name='version_number')
def get_version_number(version):
    return settings.VERSION

@register.filter(name='commit_name')
def get_commit_details(commit):
    if commit == 'url':
        return settings.COMMIT['url']
    elif commit == 'hash':
        return settings.COMMIT['hash']

@register.filter(name='nextmonth')
def next_month(month):
    if int(month) == 12:
        return 1
    month = int(month) + 1
    return month

@register.filter(name='lastmonth')
def last_month(month):
    if int(month) == 1:
        return 12
    month = int(month) - 1
    return month

@register.filter(name='lastyear')
def last_year(year, month):
    if int(month) == 1:
        year = int(year) -1
        return year
    return year

@register.filter(name='nextyear')
def next_year(year, month):
    if int(month) == 12:
        year = int(year) + 1
        return year
    return year
