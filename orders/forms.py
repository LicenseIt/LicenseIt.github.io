from django import forms
from .models import (
    Order,
    ProjectType,
    OrderDistributionIndie,
    OrderFilmMaking,
    ExternalDistribution,
    WebDistribution,
    # OrderDistributionProgramming
)  # , OrderAdvertising, OrderIndie
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


class OrderIndieForm(forms.ModelForm):
    distribution = forms.ModelMultipleChoiceField(
        queryset=OrderDistributionIndie.objects,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        CHOICES = [(0, 'No'), (1, 'Yes')]
        FILM_LENGTH = [(0, 'short film'), (1, 'full length')]
        model = OrderFilmMaking
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'form-control col-sm-8'
            }),
            'film_length': forms.Select(attrs={
                    'class': 'form-control col-sm-8'
                },
                choices=FILM_LENGTH,
            ),
            'film_programming': forms.Select(attrs={
                    'class': 'form-control col-sm-8'
                },
                choices=CHOICES,
            ),
            'film_trailer': forms.Select(attrs={
                    'class': 'form-control col-sm-8'
                },
                choices=CHOICES,
            ),
        }


class IndieWebDistribution(forms.ModelForm):
    class Meta:
        model = WebDistribution
        fields = '__all__'


class IndieExtDistribution(forms.ModelForm):
    class Meta:
        model = ExternalDistribution
        fields = '__all__'
