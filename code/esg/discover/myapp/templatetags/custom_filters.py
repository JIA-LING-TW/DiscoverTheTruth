from django import template

register = template.Library()


@register.filter
def get_dict_value(value, key):
    """
    自定義過濾器，從字典中取得指定鍵的值
    """
    if isinstance(value, dict):
        return value.get(key)
    return ''
