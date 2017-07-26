from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class ProjectType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrderIndie(models.Model):
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

    film_length = models.CharField(max_length=100)
    distribution = models.CharField(max_length=100, choices=DISTRIBUTION_CHOICES)
    number_of_viewers = models.IntegerField()
    openning_closing = models.BooleanField(default=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.production_name + ', ' + self.film_length


class OrderProgram(models.Model):
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

    distribution = models.CharField(max_length=100, choices=DISTRIBUTION_CHOICES)
    number_of_viewers = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'program: ' + self.order.production_name + ', ' + str(self.number_of_viewers)


class OrderAdvertising(models.Model):
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

    distribution = models.CharField(max_length=100, choices=DISTRIBUTION_CHOICES)
    number_of_viewers = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'advertisement: ' + self.order.production_name + ', ' + str(self.number_of_viewers)


class OrderWedding(models.Model):
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

    number_uses = models.IntegerField()
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    territory = models.CharField(max_length=2, choices=TERRITORIES_CHOICES)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'wedding: ' + self.order.production_name + ', ' + str(self.number_uses)


class Order(models.Model):
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

    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    state = models.CharField(max_length=20,
                             choices=ORDER_CHOICES,
                             default=SENT)

    song_title = models.CharField(max_length=200)
    performer_name = models.CharField(max_length=200)
    # num_of_uses = models.PositiveIntegerField()

    song_version = models.CharField(max_length=200)
    featured_background = models.CharField(max_length=20, choices=FEATURED_BACKGROUND_CHOICES)

    production_name = models.CharField(max_length=300)
    synopsis = models.TextField()
    description = models.TextField()

    trailer_full = models.CharField(max_length=20, choices=TRAILER_FULL_CHOICES)
    project_release_date = models.DateField()
    project_type = models.ForeignKey(ProjectType, related_name='general_order')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.production_name + ': ' + self.song_title
