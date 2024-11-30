from django import template

register = template.Library()


@register.filter(name='getattr')
def getattr_filter(obj, attr):
    """返回對象的屬性值"""
    return getattr(obj, attr, None)
