from django import template

register = template.Library()


@register.filter(name="classname")
def classname(obj):
    return obj.__class__.__name__

@register.filter
def modulo(number, divisor):
    return number % divisor

@register.filter
def sub(number, arg):
    return number - arg

@register.filter
def to_hex(value, digits: int):
    value = int(value)

    return f"{value:x}".rjust(digits, "0").upper()
