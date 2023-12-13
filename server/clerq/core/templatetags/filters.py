from django import template


register = template.Library()


@register.filter(name="tojs")
def tojs(value: bool) -> bool:
    """
    Convert python bool or None to js equivalent
    """
    if value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"

    raise ValueError(f"{value} is not bool")
