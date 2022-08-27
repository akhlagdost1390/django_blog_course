from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.html import format_html



# Create your models here.

class Profile(models.Model):
    THEME_CHOICES = (
        ('is-primary', 'Primary'),
        ('is-info', 'Info'),
        ('is-dark', 'Dark'),
        ('is-danger', 'Danger'),
        ('is-light', 'Light')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    birth_date = models.DateField(db_index=True, default="django.utils.timezone.now")
    phone_number = PhoneNumberField(blank=True)
    photo = models.ImageField(blank=True, upload_to="user/user_image/%Y/%m/%d/")
    theme = models.CharField(max_length=50, default="is-light", choices=THEME_CHOICES)