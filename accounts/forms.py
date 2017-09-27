from django import forms

from .models import PersonalInfo, CounterOffer, UserQuestion


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


class CounterOfferForm(forms.ModelForm):
    class Meta:
        model = CounterOffer
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'offer': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class UserQuestionForm(forms.ModelForm):
    class Meta:
        model = UserQuestion
        fields = '__all__'
