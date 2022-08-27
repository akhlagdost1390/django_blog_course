from django import template
from django.contrib.auth.models import User

register = template.Library()

def fullname(user: User) -> str:
    return f"{user.first_name} {user.last_name}".title()

register.filter('fullname', fullname)