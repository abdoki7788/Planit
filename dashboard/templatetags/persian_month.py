from django import template

register = template.Library()

@register.filter(name="pmonth")
def pmonth(m):
    months_list = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
    return months_list[m-1]
