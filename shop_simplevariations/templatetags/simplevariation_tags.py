from django import template
from shop_simplevariations.models import Option

register = template.Library()


@register.filter
def get_option_groups(value):
    """Returns all option groups for the given product."""
    return value.option_groups.all()


@register.filter
def get_options(value):
    """Returns all options for the given option group."""
    return Option.objects.filter(group=value).all()
