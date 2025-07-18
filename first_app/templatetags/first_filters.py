from django import template

register = template.Library()

@register.filter
def model_fields(obj):
    return [(field.name, getattr(obj, field.name)) for field in obj._meta.fields]