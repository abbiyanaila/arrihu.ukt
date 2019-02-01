from django import forms
from apps.member.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ['']
