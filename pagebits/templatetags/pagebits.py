from django import template

from ..models import BitGroup

register = template.Library()


@register.assignment_tag
def pagebits(slug):
    """ Return PageBits as a context variable by PageGroup slug """
    data = {}

    group = BitGroup.objects.get_group(slug=slug)

    for bit in group.bits.all():
        data[bit.context_name] = bit.resolve()

    return data
