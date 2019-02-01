from django import forms
from apps.exam.models import AssesmentWeight, LevellingInfo, Levelling


class AssesmentWeightForm(forms.ModelForm):
    class Meta:
        model = AssesmentWeight
        exclude = ['level']


class LevellingInfoForm(forms.ModelForm):
    class Meta:
        model = LevellingInfo
        fields = ['location']

class LevellingForm(forms.ModelForm):
    class Meta:
        model = Levelling
        exclude = ['profile', 'lev_info']
