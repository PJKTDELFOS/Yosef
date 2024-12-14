from django.template import Library
from django import template
from utils import tools_utils

register=Library()
@register.filter
def formata_preco(val):
    return tools_utils.formata_preco(val)