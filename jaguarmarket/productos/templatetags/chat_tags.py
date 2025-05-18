from django import template
from ..models import Mensaje

register = template.Library()

@register.filter
def unread_count(user):
    return Mensaje.objects.filter(receptor=user, leido=False).count()
