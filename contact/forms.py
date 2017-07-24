from django.forms import ModelForm, TextInput, Textarea
from .models import ContactData


class ContactForm(ModelForm):
    class Meta:
        model = ContactData
        fields = '__all__'
        widgets = {
            'full_name': TextInput(attrs={
                'id': 'senderName',
                'class': 'input-md input-rounded form-control',
                'placeholder': 'full name',
                'maxlength': 100,
            }),
            'email': TextInput(attrs={
                'type': 'email',
                'id': 'senderEmail',
                'class': "input-md input-rounded form-control",
                'placeholder': "email address",
                'max_length': 100,
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'id': 'message'
            })
        }
