from django import forms
from .models import Order, ProjectType #, OrderAdvertising, OrderIndie
# from .models import OrderProgram, OrderWedding, ProjectType


class OrderForm(forms.ModelForm):
    SENT = 'sent'
    DONE = 'done'
    ATTENTION = 'attention'

    ORDER_CHOICES = (
        (SENT, 'Sent'),
        (ATTENTION, 'Attention'),
        (DONE, 'Done'),
    )

    project_type = forms.ModelChoiceField(
        queryset=ProjectType.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        exclude = ['user', 'state']
        widgets = {
            'song_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'the song title',
            }),
            'performer_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "the performer name",
            }),
        }


#class OrderIndieForm(forms.ModelForm)