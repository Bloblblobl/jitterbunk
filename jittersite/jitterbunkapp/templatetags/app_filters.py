from django import template

register = template.Library()

@register.filter(name='authenticated')
def authenticated(value):
    return value.is_authenticated()
