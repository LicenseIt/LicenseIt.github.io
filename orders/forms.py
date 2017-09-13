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
    RateUs,
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
        widget=SelectWithTitles()
    )


class OrderForm(OrderFormBase):
    project_type = forms.ModelChoiceField(
        queryset=ProjectType.objects,
        empty_label=None,
    )

    class Meta:
        model = Order
        exclude = ['user', 'state', 'is_done']
        widgets = {
            'song': forms.HiddenInput(),
            'song_title': forms.HiddenInput(),
            'performer_name': forms.HiddenInput(),
        }


class ManualOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'state', 'song_id']
        widgets = {
            'song_title': forms.TextInput(attrs={
                'class': 'gui-input',
                'placeholder': 'song title'
            }),
            'performer_name': forms.TextInput(attrs={
                'class': "gui-input",
                'placeholder': 'performer name',
            }),
        }


class OrderIndieForm(forms.ModelForm):
    distribution = MultipleChoiceFieldWithTitles(
        queryset=OrderDistributionIndie.objects,
        widget=SelectMultipleWithTitles()
    )

    class Meta:
        model = OrderFilmMaking
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'gui-input',
                'placeholder': 'State the name of the production - typically the title of a film, video project, name of a TV show, or advertisement'
            }),
            'film_length': forms.RadioSelect(),
            'film_programming': forms.RadioSelect(),
            'film_trailer': forms.RadioSelect(),
        }


class OrderProgramForm(forms.ModelForm):
    distribution = MultipleChoiceFieldWithTitles(
        queryset=OrderDistributionProgramming.objects,
        widget=SelectMultipleWithTitles()
    )

    class Meta:
        model = OrderProgramming
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'gui-input',
                'placeholder': 'State the name of the production - typically the title of a film, video project, name of a TV show, or advertisement'
        }),
        }


class OrderAdvertisingForm(forms.ModelForm):
    distribution = MultipleChoiceFieldWithTitles(
        queryset=OrderDistributionProgramming.objects,
        widget=SelectMultipleWithTitles()
    )

    class Meta:
        model = OrderAdvertising
        fields = '__all__'
        widgets = {
            'production_name': forms.TextInput(attrs={
                'class': 'gui-input',
                'placeholder': 'State the name of the production - typically the title of a film, video project, name of a TV show, or advertisement',
            }),
        }


class IndieWebDistribution(forms.ModelForm):
    distribute_on = forms.ModelMultipleChoiceField(
        queryset=WebEntry.objects,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = WebDistribution
        fields = '__all__'
        widgets = {
            'youtube_id': forms.NumberInput(
                attrs={
                    'class': 'gui-input',
                    'placeholder': 'your youtube id...'
                }
            )
        }


class IndieExtDistribution(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        queryset=ExternalEntry.objects,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = ExternalDistribution
        fields = '__all__'
        widgets = {
            'num_people': forms.NumberInput(
                attrs={
                    'class': 'gui-input',
                    'placeholder': 'estimated answer (number)'
                }
            )
        }


class TvDistributionForm(forms.ModelForm):
    class Meta:
        model = TvDistribution
        fields = '__all__'
        widgets = {
            'tv_program': forms.CheckboxInput(),
            'tv_trailer': forms.CheckboxInput()
        }


class DetailsFormBase(forms.ModelForm):
    featured_background = forms.ModelMultipleChoiceField(
        queryset=FeaturedBackground.objects,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        widgets = {
            'number_uses': forms.NumberInput(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'opening_closing': forms.RadioSelect(
                choices=[(False, 'no'), (True, 'yes')]
            ),
            'song_version': forms.RadioSelect(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'start_duration': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'end_duration': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'term': forms.Select(),
            'territory': forms.RadioSelect(),
            'territory_usa': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'release_date': forms.DateInput(
                attrs={
                    'class': 'gui-input',
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
                    'class': 'gui-input',
                    'placeholder': 'A brief synopsis of the entire project'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'gui-textarea',
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
                    'class': 'gui-textarea',
                    'placeholder': 'Any other comments or request that you believe are important to the right owners to know'
                }
            ),
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


class RateUsForm(forms.ModelForm):
    class Meta:
        model = RateUs
        fields = '__all__'
        widgets = {
            'rate': forms.RadioSelect(
                attrs={
                    'class': 'rating-input'
                },
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
            )
        }


class WeddingDetailForm(forms.ModelForm):
    class Meta:
        model = OrderWedding
        fields = '__all__'
        widgets = {
            'platform': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'territory': forms.RadioSelect(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'territory_usa': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'num_uses': forms.NumberInput(
                attrs={
                    'class': 'gui-input'
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
                    'class': 'gui-input'
                }
            ),
            'territory': forms.RadioSelect(
                attrs={
                    'class': 'gui-inpu'
                }
            ),
            'territory_usa': forms.RadioSelect(
                attrs={
                    'class': 'gui-input'
                }
            ),
            'purpose': forms.TextInput(
                attrs={
                    'class': 'gui-input'
                }
            )
        }
