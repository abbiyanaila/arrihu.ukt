from django import forms
from django.contrib.auth.models import User
from core.models import Setting


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    class Meta:
        model = User


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = ['']
