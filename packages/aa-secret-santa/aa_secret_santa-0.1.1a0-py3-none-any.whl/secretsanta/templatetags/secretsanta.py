from typing import Union

from django import template
from django.contrib.auth.models import User

from secretsanta.models import Application, SantaPair, Year

register = template.Library()

_BASE_URL = 'http://evemaps.dotlan.net'


@register.simple_tag()
def application_exists(year: Year, user: User) -> bool:
    try:
        if Application.objects.filter(year=year, user=user).exists():
            return True
        else:
            return False
    except Exception:
        return False


@register.simple_tag()
def get_users_santee(year: Year, user: User) -> Union[User, str]:
    try:
        return SantaPair.objects.get(year=year, santa=user).santee
    except SantaPair.DoesNotExist:
        try:
            if application_exists(year=year, user=user):
                return "Not Yet Assigned"
            else:
                ""
        except Exception:
            return ""
        return ""
