from django import forms
from apps.member.models import Division, Level


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        exclude = ['']


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        exclude = ['division']

