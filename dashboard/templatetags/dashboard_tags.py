from django import template

register = template.Library()


@register.filter
def intcomma(value):
    try:
        return f"{int(value):,}".replace(',', '\u202f')
    except (TypeError, ValueError):
        return value


@register.filter
def pct(value, total):
    try:
        return round(int(value) / int(total) * 100, 1)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0
