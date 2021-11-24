from django import template
from core.models import Item

register = template.Library()

@register.filter
def in_category(category):
    if category:
        return Item.objects.filter(category=category.upper())
    return Item.objects.all()