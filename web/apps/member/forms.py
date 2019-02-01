from django import forms
from apps.member.models import Physic, Profile, Level


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('pria', 'Pria'),
        ('wanita', 'Wanita'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Profile
        exclude = ['user', 'physic', 'gender', 'qrcode']
        widgets = {
            'born_date': DateInput()
        }


class PhysicForm(forms.ModelForm):
    class Meta:
        model = Physic
        exclude = ['']

