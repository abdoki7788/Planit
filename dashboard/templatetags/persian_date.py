from django import template
from . import persian_month, persian_number

register = template.Library()

@register.filter(name="pdate")
def pdate(date):
    return persian_number.persianize(f"{date.day} {persian_month.pmonth(date.month)} {date.year}")

