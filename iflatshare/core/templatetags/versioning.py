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
