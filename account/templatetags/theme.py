from django import template
from django.contrib.auth.models import User

register = template.Library()

def theme(user: User):
    if user.is_authenticated:
        return user.profile.theme
    return "is-light"

register.filter('theme', theme)