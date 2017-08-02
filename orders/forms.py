from django import forms
from .models import (
    Order,
    ProjectType,
    OrderDistributionIndie,
    OrderFilmMaking,
    ExternalDistribution,
    WebDistribution,
    WebEntry,
    ExternalEntry,
    OrderIndieProjectDetail,
    FeaturedBackground,
)


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
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        model = OrderFilmMaking
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'form-control col-sm-8'
            }),
            'film_length': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-8'
                },
            ),
            'film_programming': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-8'
                },
            ),
            'film_trailer': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-8'
                },
            ),
        }


class IndieWebDistribution(forms.ModelForm):
    distribute_on = forms.ModelMultipleChoiceField(
        queryset=WebEntry.objects,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        model = WebDistribution
        fields = '__all__'
        widgets = {
            'youtube_id': forms.NumberInput(
                attrs={
                    'class': 'form-control col-sm-2'
                }
            )
        }


class IndieExtDistribution(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        queryset=ExternalEntry.objects,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        model = ExternalDistribution
        fields = '__all__'
        widgets = {
            'num_people': forms.NumberInput(
                attrs={
                    'class': 'form-control col-sm-2'
                }
            )
        }


class IndieDetailForm(forms.ModelForm):
    featured_background = forms.ModelMultipleChoiceField(
        queryset=FeaturedBackground.objects,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        model = OrderIndieProjectDetail
        fields = '__all__'
        widgets = {
            'number_uses': forms.NumberInput(
                attrs={
                    'class': 'form-control col-sm-2'
                }
            ),
            'opening_closing': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-3'
                },
                choices=[(False, 'no'), (True, 'yes')]
            ),
            'song_version': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'duration': forms.NumberInput(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'term': forms.Select(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'territory': forms.RadioSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'release_date': forms.DateInput(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'budget': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'synopsis': forms.TextInput(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'is_non_profit': forms.CheckboxInput(
                attrs={
                    'class': 'form-control col-sm-1'
                }
            ),
            'non_profit': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'comments': forms.Textarea(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'rate': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-3'
                },
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
            )
        }
