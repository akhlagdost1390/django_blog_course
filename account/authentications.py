from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import Profile


class EmailAuthenticate(BaseBackend):
    def authenticate(self, request: HttpRequest, username=None, password=None):
        try:
            user: User = User.objects.get(email=username)
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class PhoneAuthenticate(BaseBackend):
    def authenticate(self, request: HttpRequest, username=None, password=None):
        try:
            profile = Profile.objects.get(phone_number=username)
            user: User = profile.user
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        