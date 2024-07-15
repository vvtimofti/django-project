from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def custom_naturaltime(value):
    natural_time = timesince(value)

    natural_time = natural_time.replace('hour', 'h').replace(
        'minute', 'm').replace('day', 'd').replace('week', 'w').replace('month', 'mon').replace('year', 'y')

    first_two_words = ''.join(natural_time.split()[:2]).rstrip('s,')
    return first_two_words
