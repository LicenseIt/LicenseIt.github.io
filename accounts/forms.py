from django import forms

from .models import PersonalInfo


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        widgets = {
            'address': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            )
        }
