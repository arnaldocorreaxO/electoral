from django import template
from django.forms import CheckboxInput

from core.security.models import Module
from core.security.models import ModuleType

register = template.Library()


@register.filter
def getmoduletype(group_id):
    return ModuleType.objects.filter(module__groupmodule__group_id=group_id, is_active=True).distinct().order_by(
        'name')


@register.filter()
def getmodulehorizontal(group):
    return Module.objects.filter(groupmodule__group_id=group, moduletype_id=None, is_active=True,
                                 is_vertical=False).order_by('name')


@register.filter()
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__