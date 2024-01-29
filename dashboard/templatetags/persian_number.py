from django import template
import persian

register = template.Library()

def persianize(value, *args, **kwargs):
    return persian.convert_en_numbers(value)

register.filter("persianize", persianize)
