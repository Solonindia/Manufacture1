from django import template

register = template.Library()

@register.filter
def format_time(value):
    if value is not None:
        return value.strftime('%I:%M %p')
    return ''
