from django import forms
from .models import Order, OrderAdvertising, OrderIndie
from .models import OrderProgram, OrderWedding, ProjectType


class OrderForm(forms.ModelForm):
    SENT = 'sent'
    DONE = 'done'
    ATTENTION = 'attention'

    ORDER_CHOICES = (
        (SENT, 'Sent'),
        (ATTENTION, 'Attention'),
        (DONE, 'Done'),
    )

    FEATURED = 'fg'
    BACKGROUND = 'bg'

    FEATURED_BACKGROUND_CHOICES = (
        (FEATURED, 'featured'),
        (BACKGROUND, 'background')
    )

    TRAILER_FULL_CHOICES = (
        ('trailer', 'trailer'),
        ('full', 'full movie'),
        ('both', 'both')
    )

    project_type = forms.ModelChoiceField(
        queryset=ProjectType.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}))
    featured_background = forms.CharField(
        widget=forms.Select(
            choices=FEATURED_BACKGROUND_CHOICES,
            attrs={'class': 'form-control'}))
    trailer_full = forms.CharField(
        widget=forms.Select(
            choices=TRAILER_FULL_CHOICES,
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
            'song_version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'song version'
            }),
            'production_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'production name'
            }),
            'project_release_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'project release date'
            }),
            'synopsis': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }


class OrderAdvertiseForm(forms.ModelForm):
    DISTRIBUTION_CHOICES = (
        (
            'web', (
                ('youtube', 'youtube'),
                ('vimeo', 'vimeo'),
                ('vine', 'vine'),
                ('facebook', 'facebook'),
                ('web_other', 'other')
            )
        ),
        ('tv', 'tv'),
        ('podcast', 'podcast'),
        ('theaters', 'theaters'),
        ('mobile', 'mobile'),
        ('radio', 'radio'),
        ('console', 'game consoles'),
        ('internal', 'internally'),
        (
            'external', (
                ('festival', 'film festival entry'),
                ('conf', 'conferences'),
                ('no-theater', 'non-theateratically distributed viewing'),
                ('events', 'events'),
                ('tradeshow', 'trade shows'),
                ('ex_other', 'other')
            )
        ),
        ('other', 'other')
    )

    distribution = forms.SelectMultiple(choices=DISTRIBUTION_CHOICES,
                                        attrs={'class': 'form-control'})

    class Meta:
        model = OrderAdvertising
        fields = '__all__'
        widgets = {
            'number_of_viewers': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class OrderIndieForm(forms.ModelForm):
    DISTRIBUTION_CHOICES = (
        (
            'web', (
                ('youtube', 'youtube'),
                ('vimeo', 'vimeo'),
                ('vine', 'vine'),
                ('facebook', 'facebook'),
                ('web_other', 'other')
            )
        ),
        (
            'externally', (
                ('festival', 'film festival entry'),
                ('conf', 'conferences'),
                ('no-theater', 'non-theateratically distributed viewing'),
                ('events', 'events'),
                ('tradeshow', 'trade shows'),
                ('ex_other', 'other')
            )
        ),
        ('broadcast', 'broadcast media'),
        ('theaters', 'theaters'),
        ('other', 'other')
    )

    distribution = forms.ChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        choices=DISTRIBUTION_CHOICES)

    class Meta:
        model = OrderIndie
        fields = '__all__'
        widgets = {
            'film_length': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'number_of_viewers': forms.TextInput(attrs={'class': 'form-control'}),
            'openning_closing': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class OrderProgramForm(forms.ModelForm):
    DISTRIBUTION_CHOICES = (
        (
            'web', (
                ('site', 'site/sites'),
                ('games', 'games'),
                ('web_other', 'other')
            )
        ),
        ('mobile', 'mobile'),
        ('desktop', 'desktop'),
        ('console', 'game consoles'),
        ('internal', 'internally'),
        ('external', 'externally'),
        ('other', 'other')
    )

    distribution = forms.MultipleChoiceField(
        choices=DISTRIBUTION_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-input'}))

    class Meta:
        model = OrderProgram
        fields = '__all__'
        widgets = {
            'number_of_viewers': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrderWeddingForm(forms.ModelForm):
    BUDGET_CHOICES = (
        ('low', '0-$50K'),
        ('medium', '$50K-$250K'),
        ('high', '$250K-$500K'),
        ('very', '$500K+')
    )

    TERRITORIES_CHOICES = (
        ('AW', 'Aruba'),
        ('AF', 'Afghanistan'),
        ('AO', 'Angola'),
        ('AI', 'Anguilla'),
        ('AX', '\xc5land Islands'),
        ('AL', 'Albania'),
        ('AD', 'Andorra'),
        ('AE', 'United Arab Emirates'),
        ('AR', 'Argentina'),
        ('AM', 'Armenia'),
        ('AS', 'American Samoa'),
        ('AQ', 'Antarctica'),
        ('TF', 'French Southern Territories'),
        ('AG', 'Antigua and Barbuda'),
        ('AU', 'Australia'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BI', 'Burundi'),
        ('BE', 'Belgium'),
        ('BJ', 'Benin'),
        ('BQ', 'Bonaire, Sint Eustatius and Saba'),
        ('BF', 'Burkina Faso'),
        ('BD', 'Bangladesh'),
        ('BG', 'Bulgaria'),
        ('BH', 'Bahrain'),
        ('BS', 'Bahamas'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BL', 'Saint Barth\xe9lemy'),
        ('BY', 'Belarus'),
        ('BZ', 'Belize'),
        ('BM', 'Bermuda'),
        ('BO', 'Bolivia, Plurinational State of'),
        ('BR', 'Brazil'),
        ('BB', 'Barbados'),
        ('BN', 'Brunei Darussalam'),
        ('BT', 'Bhutan'),
        ('BV', 'Bouvet Island'),
        ('BW', 'Botswana'),
        ('CF', 'Central African Republic'),
        ('CA', 'Canada'),
        ('CC', 'Cocos (Keeling) Islands'),
        ('CH', 'Switzerland'),
        ('CL', 'Chile'),
        ('CN', 'China'),
        ('CI', "C\xf4te d'Ivoire"),
        ('CM', 'Cameroon'),
        ('CD', 'Congo, The Democratic Republic of the'),
        ('CG', 'Congo'),
        ('CK', 'Cook Islands'),
        ('CO', 'Colombia'),
        ('KM', 'Comoros'),
        ('CV', 'Cabo Verde'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('CW', 'Cura\xe7ao'),
        ('CX', 'Christmas Island'),
        ('KY', 'Cayman Islands'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czechia'),
        ('DE', 'Germany'),
        ('DJ', 'Djibouti'),
        ('DM', 'Dominica'),
        ('DK', 'Denmark'),
        ('DO', 'Dominican Republic'),
        ('DZ', 'Algeria'),
        ('EC', 'Ecuador'),
        ('EG', 'Egypt'),
        ('ER', 'Eritrea'),
        ('EH', 'Western Sahara'),
        ('ES', 'Spain'),
        ('EE', 'Estonia'),
        ('ET', 'Ethiopia'),
        ('FI', 'Finland'),
        ('FJ', 'Fiji'),
        ('FK', 'Falkland Islands (Malvinas)'),
        ('FR', 'France'),
        ('FO', 'Faroe Islands'),
        ('FM', 'Micronesia, Federated States of'),
        ('GA', 'Gabon'),
        ('GB', 'United Kingdom'),
        ('GE', 'Georgia'),
        ('GG', 'Guernsey'),
        ('GH', 'Ghana'),
        ('GI', 'Gibraltar'),
        ('GN', 'Guinea'),
        ('GP', 'Guadeloupe'),
        ('GM', 'Gambia'),
        ('GW', 'Guinea-Bissau'),
        ('GQ', 'Equatorial Guinea'),
        ('GR', 'Greece'),
        ('GD', 'Grenada'),
        ('GL', 'Greenland'),
        ('GT', 'Guatemala'),
        ('GF', 'French Guiana'),
        ('GU', 'Guam'),
        ('GY', 'Guyana'),
        ('HK', 'Hong Kong'),
        ('HM', 'Heard Island and McDonald Islands'),
        ('HN', 'Honduras'),
        ('HR', 'Croatia'),
        ('HT', 'Haiti'),
        ('HU', 'Hungary'),
        ('ID', 'Indonesia'),
        ('IM', 'Isle of Man'),
        ('IN', 'India'),
        ('IO', 'British Indian Ocean Territory'),
        ('IE', 'Ireland'),
        ('IR', 'Iran, Islamic Republic of'),
        ('IQ', 'Iraq'),
        ('IS', 'Iceland'),
        ('IL', 'Israel'),
        ('IT', 'Italy'),
        ('JM', 'Jamaica'),
        ('JE', 'Jersey'),
        ('JO', 'Jordan'),
        ('JP', 'Japan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KG', 'Kyrgyzstan'),
        ('KH', 'Cambodia'),
        ('KI', 'Kiribati'),
        ('KN', 'Saint Kitts and Nevis'),
        ('KR', 'Korea, Republic of'),
        ('KW', 'Kuwait'),
        ('LA', "Lao People's Democratic Republic"),
        ('LB', 'Lebanon'),
        ('LR', 'Liberia'),
        ('LY', 'Libya'),
        ('LC', 'Saint Lucia'),
        ('LI', 'Liechtenstein'),
        ('LK', 'Sri Lanka'),
        ('LS', 'Lesotho'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('LV', 'Latvia'),
        ('MO', 'Macao'),
        ('MF', 'Saint Martin (French part)'),
        ('MA', 'Morocco'),
        ('MC', 'Monaco'),
        ('MD', 'Moldova, Republic of'),
        ('MG', 'Madagascar'),
        ('MV', 'Maldives'),
        ('MX', 'Mexico'),
        ('MH', 'Marshall Islands'),
        ('MK', 'Macedonia, Republic of'),
        ('ML', 'Mali'),
        ('MT', 'Malta'),
        ('MM', 'Myanmar'),
        ('ME', 'Montenegro'),
        ('MN', 'Mongolia'),
        ('MP', 'Northern Mariana Islands'),
        ('MZ', 'Mozambique'),
        ('MR', 'Mauritania'),
        ('MS', 'Montserrat'),
        ('MQ', 'Martinique'),
        ('MU', 'Mauritius'),
        ('MW', 'Malawi'),
        ('MY', 'Malaysia'),
        ('YT', 'Mayotte'),
        ('NA', 'Namibia'),
        ('NC', 'New Caledonia'),
        ('NE', 'Niger'),
        ('NF', 'Norfolk Island'),
        ('NG', 'Nigeria'),
        ('NI', 'Nicaragua'),
        ('NU', 'Niue'),
        ('NL', 'Netherlands'),
        ('NO', 'Norway'),
        ('NP', 'Nepal'),
        ('NR', 'Nauru'),
        ('NZ', 'New Zealand'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PA', 'Panama'),
        ('PN', 'Pitcairn'),
        ('PE', 'Peru'),
        ('PH', 'Philippines'),
        ('PW', 'Palau'),
        ('PG', 'Papua New Guinea'),
        ('PL', 'Poland'),
        ('PR', 'Puerto Rico'),
        ('KP', "Korea, Democratic People's Republic of"),
        ('PT', 'Portugal'),
        ('PY', 'Paraguay'),
        ('PS', 'Palestine, State of'),
        ('PF', 'French Polynesia'),
        ('QA', 'Qatar'),
        ('RE', 'R\xe9union'),
        ('RO', 'Romania'),
        ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'),
        ('SA', 'Saudi Arabia'),
        ('SD', 'Sudan'),
        ('SN', 'Senegal'),
        ('SG', 'Singapore'),
        ('GS', 'South Georgia and the South Sandwich Islands'),
        ('SH', 'Saint Helena, Ascension and Tristan da Cunha'),
        ('SJ', 'Svalbard and Jan Mayen'),
        ('SB', 'Solomon Islands'),
        ('SL', 'Sierra Leone'),
        ('SV', 'El Salvador'),
        ('SM', 'San Marino'),
        ('SO', 'Somalia'),
        ('PM', 'Saint Pierre and Miquelon'),
        ('RS', 'Serbia'),
        ('SS', 'South Sudan'),
        ('ST', 'Sao Tome and Principe'),
        ('SR', 'Suriname'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('SE', 'Sweden'),
        ('SZ', 'Swaziland'),
        ('SX', 'Sint Maarten (Dutch part)'),
        ('SC', 'Seychelles'),
        ('SY', 'Syrian Arab Republic'),
        ('TC', 'Turks and Caicos Islands'),
        ('TD', 'Chad'),
        ('TG', 'Togo'),
        ('TH', 'Thailand'),
        ('TJ', 'Tajikistan'),
        ('TK', 'Tokelau'),
        ('TM', 'Turkmenistan'),
        ('TL', 'Timor-Leste'),
        ('TO', 'Tonga'),
        ('TT', 'Trinidad and Tobago'),
        ('TN', 'Tunisia'),
        ('TR', 'Turkey'),
        ('TV', 'Tuvalu'),
        ('TW', 'Taiwan, Province of China'),
        ('TZ', 'Tanzania, United Republic of'),
        ('UG', 'Uganda'),
        ('UA', 'Ukraine'),
        ('UM', 'United States Minor Outlying Islands'),
        ('UY', 'Uruguay'),
        ('US', 'United States'),
        ('UZ', 'Uzbekistan'),
        ('VA', 'Holy See (Vatican City State)'),
        ('VC', 'Saint Vincent and the Grenadines'),
        ('VE', 'Venezuela, Bolivarian Republic of'),
        ('VG', 'Virgin Islands, British'),
        ('VI', 'Virgin Islands, U.S.'),
        ('VN', 'Viet Nam'),
        ('VU', 'Vanuatu'),
        ('WF', 'Wallis and Futuna'),
        ('WS', 'Samoa'),
        ('YE', 'Yemen'),
        ('ZA', 'South Africa'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe')
    )

    budget = forms.MultipleChoiceField(
        choices=BUDGET_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-input'}))
    territories = forms.MultipleChoiceField(
        choices=TERRITORIES_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-input'}))

    class Meta:
        model = OrderWedding
        fields = '__all__'
        widgets = {
            'number_uses': forms.TextInput(attrs={'class': 'form-control'})
        }
