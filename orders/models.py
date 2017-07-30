from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    '''
    base class for all models of orders
    '''
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProjectType(Base):
    '''
    type of project the user is working on
    '''
    name = models.CharField(max_length=200)
    # the url name of the type to work with on the back end
    slug = models.SlugField()

    def __str__(self):
        return self.name


class DistributionBase(Base):
    '''
    
    '''
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class EntriesBase(Base):
    '''
    the entries on each of the categories
    '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class WebEntries(EntriesBase):
    pass


class ExternalEntries(EntriesBase):
    pass


class OrderDistributionIndie(DistributionBase):
    pass


class OrderDistributionProgramming(DistributionBase):
    pass


class WebDistribution(Base):
    distribute_on = models.ManyToManyField(WebEntries, related_name='dist_web')
    youtube_id = models.IntegerField(null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_dist_web')

    def __str__(self):
        return self.distribute_on.name


class ExternalDistribution(Base):
    name = models.ManyToManyField(ExternalEntries, related_name='ext_dist')
    num_people = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TvDistribution(Base):
    tv_program = models.BooleanField()
    tv_trailer = models.BooleanField()

    def __str__(self):
        return 'program: ' + str(self.tv_program) + 'trailer: ' + str(self.tv_trailer)


class OrderProjectDetailsBase(Base):
    COUNTRIES_CHOICES = [
        ('EA', 'All countries'),
        ('A1', 'Asia'),
        ('EU', 'Europe'),
        ('NT', 'North America'),
        ('SU', 'South America'),
        ('A5', 'Australia'),
        ('A3', 'Africa'),
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
    ]

    USA_CHOICES = [
        ('US-WI', 'Wisconsin'),
        ('US-WV', 'West Virginia'),
        ('US-MI', 'Michigan'),
        ('US-OK', 'Oklahoma'),
        ('US-MN', 'Minnesota'),
        ('US-MO', 'Missouri'),
        ('US-NJ', 'New Jersey'),
        ('US-VT', 'Vermont'),
        ('US-MS', 'Mississippi'),
        ('US-SD', 'South Dakota'),
        ('US-MT', 'Montana'),
        ('US-NC', 'North Carolina'),
        ('US-OR', 'Oregon'),
        ('US-VA', 'Virginia'),
        ('US-AK', 'Alaska'),
        ('US-AL', 'Alabama'),
        ('US-NM', 'New Mexico'),
        ('US-AR', 'Arkansas'),
        ('US-WY', 'Wyoming'),
        ('US-TN', 'Tennessee'),
        ('US-AZ', 'Arizona'),
        ('US-CA', 'California'),
        ('US-PA', 'Pennsylvania'),
        ('US-CO', 'Colorado'),
        ('US-CT', 'Connecticut'),
        ('US-NV', 'Nevada'),
        ('US-DE', 'Delaware'),
        ('US-ND', 'North Dakota'),
        ('US-WA', 'Washington'),
        ('US-FL', 'Florida'),
        ('US-GA', 'Georgia'),
        ('US-HI', 'Hawaii'),
        ('US-NY', 'New York'),
        ('US-IA', 'Iowa'),
        ('US-ID', 'Idaho'),
        ('US-NE', 'Nebraska'),
        ('US-IL', 'Illinois'),
        ('US-IN', 'Indiana'),
        ('US-RI', 'Rhode Island'),
        ('US-UT', 'Utah'),
        ('US-KS', 'Kansas'),
        ('US-KY', 'Kentucky'),
        ('US-OH', 'Ohio'),
        ('US-LA', 'Louisiana'),
        ('US-MA', 'Massachusetts'),
        ('US-NH', 'New Hampshire'),
        ('US-TX', 'Texas'),
        ('US-MD', 'Maryland'),
        ('US-ME', 'Maine'),
        ('US-SC', 'South Carolina'),
    ]

    territory = models.CharField(max_length=2, choices=COUNTRIES_CHOICES)
    territory_usa = models.CharField(max_length=5, choices=USA_CHOICES, null=True, blank=True)

    class Meta:
        abstract = True


class OrderProjectBase(Base):
    production_name = models.CharField(max_length=300)
    distribution = models.ManyToManyField(OrderDistributionProgramming,
                                          related_name='order_dist_%(class)s')
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='order_project_%(class)s')

    class Meta:
        abstract = True


class OrderFilmMaking(OrderProjectBase):
    # should be radio buttons
    film_length = models.BooleanField()
    # should be radio, yes/no
    film_programming = models.BooleanField()
    film_trailer = models.BooleanField()

    def __str__(self):
        return 'indie movie' + self.production_name


class FeaturedBackground(Base):
    name = models.CharField(max_length=100)

    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderProgramming(OrderProjectBase):
    pass


class OrderAdvertising(OrderProjectBase):
    pass


class ProjectDetailsBase(Base):
    ORIGINAL = 'original'
    INSTRUMENTAL = 'instrumental'
    CAPELLA = 'capella'
    OTHER = 'other'

    SONG_VERSION_CHOICES = (
        (ORIGINAL, 'original recording'),
        (INSTRUMENTAL, 'instrumental version'),
        (CAPELLA, 'capella version'),
        (OTHER, 'other')
    )

    DAY1 = '1d'
    DAY3 = '3d'
    WEEK1 = '1w'
    WEEK2 = '2w'
    MONTH1 = '1m'
    MONTH3 = '3m'
    MONTH6 = '6m'
    YEAR1 = '1y'
    YEAR2 = '2y'
    UNLIMITED = 'no'

    TERM_CHOICES = (
        (DAY1, '1 day'),
        (DAY3, '3 day'),
        (WEEK1, '1 week'),
        (WEEK2, '2 weeks'),
        (MONTH1, '1 month'),
        (MONTH3, '3 months'),
        (MONTH6, '6 months'),
        (YEAR1, '1 year'),
        (YEAR2, '2 years'),
        (UNLIMITED, 'In Perpetuity (not time-limited)'),
    )

    BUDGET_CHOICES = [
        ('low', '$0-50k Budget'),
        ('med', '$50-250k Budget'),
        ('high', '$250-500k Budget'),
        ('very', '$500k+ Budget'),
    ]

    NON_PROFIT_CHOICES = [
        ('edu', 'School/University'),
        ('rlg', 'Church'),
        ('tax', '501c3 or International Equivalent'),
        ('oth', 'Other'),
    ]

    number_uses = models.IntegerField()
    opening_closing = models.BooleanField()
    featured_background = models.ManyToManyField(FeaturedBackground,
                                                 related_name='programming_project_details_%(class)s')
    song_version = models.CharField(max_length=20, choices=SONG_VERSION_CHOICES)

    # need to check what he wants
    duration = models.IntegerField()
    term = models.CharField(max_length=2, choices=TERM_CHOICES, default=YEAR1)

    release_date = models.DateField()
    budget = models.CharField(max_length=5, choices=BUDGET_CHOICES)

    synopsis = models.CharField(max_length=1000)
    description = models.TextField()

    is_non_profit = models.BooleanField()
    non_profit = models.CharField(max_length=3, choices=NON_PROFIT_CHOICES,
                                  null=True, blank=True)

    comments = models.TextField()

    rate = models.SmallIntegerField()

    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return 'details for project: %(class)s- ' + self.order.song_title

    class Meta:
        abstract = True


class OrderIndieProjectDetails(ProjectDetailsBase):
    pass


class OrderProgrammingDetails(ProjectDetailsBase):
    pass


class OrderAdvertisingDetails(ProjectDetailsBase):
    pass


class OrderWedding(OrderProjectDetailsBase):
    platform = models.CharField(max_length=1000)
    num_uses = models.PositiveIntegerField()


class OrderPersonal(OrderProjectDetailsBase):
    purpose = models.CharField(max_length=1000)
    platform = models.CharField(max_length=1000)


class Order(Base):
    SENT = 'sent'
    DONE = 'done'
    ATTENTION = 'attention'

    ORDER_CHOICES = (
        (SENT, 'Sent'),
        (ATTENTION, 'Attention'),
        (DONE, 'Done'),
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

    project_type = models.ForeignKey(ProjectType, related_name='general_order')

    def __str__(self):
        return str(self.id) + ': ' + self.song_title
