from django import template

register = template.Library()


@register.filter()
def number_format(value):
    return "{:,.2f}".format(value)
