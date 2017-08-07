from django import forms

from common.form_widgets import SelectMultipleWithTitles, MultipleChoiceFieldWithTitles
from common.form_widgets import SelectWithTitles, ChoiceFieldWithTitles

from .models import (
    Order,
    ProjectType,
    OrderDistributionIndie,
    OrderFilmMaking,
    OrderProgramming,
    OrderAdvertising,
    ExternalDistribution,
    WebDistribution,
    WebEntry,
    ExternalEntry,
    TvDistribution,
    OrderIndieProjectDetail,
    OrderProgrammingDetail,
    OrderAdvertisingDetail,
    OrderWedding,
    OrderPersonal,
    FeaturedBackground,
    OrderDistributionProgramming,
)


class OrderFormBase(forms.ModelForm):
    SENT = 'sent'
    DONE = 'done'
    ATTENTION = 'attention'

    ORDER_CHOICES = (
        (SENT, 'Sent'),
        (ATTENTION, 'Attention'),
        (DONE, 'Done'),
    )

    project_type = ChoiceFieldWithTitles(
        queryset=ProjectType.objects,
        widget=SelectWithTitles(
            attrs={
                'class': 'form-control',
            }
        )
    )


class OrderForm(OrderFormBase):
    project_type = forms.ModelChoiceField(
        queryset=ProjectType.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = Order
        exclude = ['user', 'state']
        widgets = {
            'song': forms.HiddenInput(),
            'song_title': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'true'
            }),
            'performer_name': forms.TextInput(attrs={
                'class': "form-control",
                'readonly': "true",
            }),
        }


class ManualOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'state']
        widgets = {
            'song_title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'performer_name': forms.TextInput(attrs={
                'class': "form-control",
            }),
        }


class OrderIndieForm(forms.ModelForm):
    distribution = MultipleChoiceFieldWithTitles(
        queryset=OrderDistributionIndie.objects,
        widget=SelectMultipleWithTitles(
            attrs={
                'class': 'form-control col-sm-8',
            }
        )
    )

    class Meta:
        model = OrderFilmMaking
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'form-control col-sm-8',
                'placeholder': 'State the name of the production - typically the title of a film, video project, name of a TV show, or advertisement'
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


class OrderProgramForm(forms.ModelForm):
    distribution = MultipleChoiceFieldWithTitles(
        queryset=OrderDistributionProgramming.objects,
        widget=SelectMultipleWithTitles(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        model = OrderProgramming
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'form-control col-sm-8',
                'placeholder': 'State the name of the production - typically the title of a film, video project, name of a TV show, or advertisement'
        }),
        }


class OrderAdvertisingForm(forms.ModelForm):
    distribution = MultipleChoiceFieldWithTitles(
        queryset=OrderDistributionProgramming.objects,
        widget=SelectMultipleWithTitles(
            attrs={
                'class': 'form-control col-sm-8'
            }
        )
    )

    class Meta:
        model = OrderAdvertising
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'form-control col-sm-8',
                'placeholder': 'State the name of the production - typically the title of a film, video project, name of a TV show, or advertisement',
            }),
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


class TvDistributionForm(forms.ModelForm):
    class Meta:
        model = TvDistribution
        fields = '__all__'
        widgets = {
            'tv_program': forms.CheckboxInput(
                attrs={
                    'class': 'form-control col-sm-2'
                }
            ),
            'tv_trailer': forms.CheckboxInput(
                attrs={
                    'class': 'form-control col-sm-2'
                }
            )
        }


class DetailsFormBase(forms.ModelForm):
    featured_background = forms.ModelMultipleChoiceField(
        queryset=FeaturedBackground.objects,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-control col-sm-8',
            }
        )
    )

    class Meta:
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
            'start_duration': forms.TextInput(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'end_duration': forms.TextInput(
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
            'territory_usa': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'release_date': forms.DateInput(
                attrs={
                    'class': 'form-control col-sm-3',
                    'title': 'if no, just type your estimation',
                }
            ),
            'budget': SelectWithTitles(
                attrs={
                    'class': 'form-control col-sm-3'
                }
            ),
            'synopsis': forms.TextInput(
                attrs={
                    'class': 'form-control col-sm-3',
                    'placeholder': 'A brief synopsis of the entire project'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control col-sm-3',
                    'placeholder': 'A description of the particular scene with the music'
                }
            ),
            'is_non_profit': forms.RadioSelect(
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
                    'class': 'form-control col-sm-3',
                    'placeholder': 'Any other comments or request that you believe are important to the right owners to know'
                }
            ),
            'rate': forms.RadioSelect(
                attrs={
                    'class': 'form-control col-sm-3'
                },
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
            )
        }


class IndieDetailForm(DetailsFormBase):
    class Meta(DetailsFormBase.Meta):
        model = OrderIndieProjectDetail
        fields = '__all__'


class ProgramDetailForm(DetailsFormBase):
    class Meta(DetailsFormBase.Meta):
        model = OrderProgrammingDetail
        fields = '__all__'


class AdvertisingDetailForm(DetailsFormBase):
    class Meta(DetailsFormBase.Meta):
        model = OrderAdvertisingDetail
        fields = '__all__'


class WeddingDetailForm(forms.ModelForm):
    class Meta:
        model = OrderWedding
        fields = '__all__'
        widgets = {
            'platform': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'territory': forms.RadioSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'territory_usa': forms.RadioSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'num_uses': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = OrderPersonal
        fields = '__all__'
        widgets = {
            'platform': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'territory': forms.RadioSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'territory_usa': forms.RadioSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'purpose': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
