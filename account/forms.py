from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'theme')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input'}),
            'photo': forms.FileInput(attrs={'class': 'input'}),
            'birth_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'})
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(ProfileRegisterForm):
    pass


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('theme',)
        widgets = {
            'theme': forms.RadioSelect(attrs={"class": "block"})
        }
        labels = {
            'theme': ""
        }
