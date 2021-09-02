from shop import models
from django import template
from ..models import Product

register = template.Library()

def get_count(value, dict):
    return dict[value]


register.filter('get_count', get_count)
