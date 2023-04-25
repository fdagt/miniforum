from django import template

register = template.Library()

@register.simple_tag
def serial_number(per_page, page, counter):
    return per_page * (page - 1) + counter
