from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from search.models import Track


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
    type of project we use for questions
    '''
    name = models.CharField(max_length=200)
    # the url name of the type to work with on the back end
    slug = models.SlugField()
    # the explanation for the field
    explanation = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'project type'
        verbose_name_plural = 'project types'


class DistributionBase(Base):
    '''
    name of the distribution categories
    '''
    name = models.CharField(max_length=200)
    explanation = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class EntryBase(Base):
    '''
    the entries on each of the categories
    '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class WebEntry(EntryBase):
    '''
    a web entry name to choose on where the user will publish the work
    '''
    class Meta:
        verbose_name = 'web entry'
        verbose_name_plural = 'web entries'


class ExternalEntry(EntryBase):
    '''
    an external option on where to publish the work
    '''
    class Meta:
        verbose_name = 'external entry'
        verbose_name_plural = 'external entries'


class OrderDistributionIndie(DistributionBase):
    '''
    the options film making creators will be able to choose on where they publish their work
    '''
    class Meta:
        verbose_name = 'indie film distribution option'
        verbose_name_plural = 'indie film distribution options'


class OrderDistributionProgramming(DistributionBase):
    '''
    the options programmer creators will be able to choose on where they publish their work
    '''
    class Meta:
        verbose_name = 'programming distribution option'
        verbose_name_plural = 'programming distribution options'


class WebDistribution(Base):
    '''
    the places the publisher will publish on the web
    '''
    distribute_on = models.ManyToManyField(WebEntry, related_name='dist_web')
    youtube_id = models.IntegerField(null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_dist_web')

    def __str__(self):
        ret = ''
        for name in self.distribute_on.all():
            ret += ', ' + name.name
        return ret

    class Meta:
        verbose_name = 'web distribution'
        verbose_name_plural = 'web distributions'


class ExternalDistribution(Base):
    '''
    the kind of events the publisher will publish his/her work
    '''
    name = models.ManyToManyField(ExternalEntry, related_name='ext_dist')
    num_people = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_dist_ext')

    def __str__(self):
        ret = ''
        for name in self.name.all():
            ret += name.name + ' '
        return ret

    class Meta:
        verbose_name = 'external distribution'
        verbose_name_plural = 'external distributions'


class TvDistribution(Base):
    '''
    the kind of tv distribution of the publisher
    '''
    tv_program = models.BooleanField()
    tv_trailer = models.BooleanField()

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_tv_dist')

    def __str__(self):
        return 'program: ' + str(self.tv_program) + 'trailer: ' + str(self.tv_trailer)

    class Meta:
        verbose_name = 'tv distribution'
        verbose_name_plural = 'tv distributions'


class OrderProjectDetailBase(Base):
    '''
    base class for all other details classes
    '''
    COUNTRIES_CHOICES = [
        ('worldwide', 'worldwide'),
        ('Asia', 'Asia'),
        ('Europe', 'Europe'),
        ('North America', 'North America'),
        ('South America', 'South America'),
        ('Australia', 'Australia'),
        ('Africa', 'Africa'),
        ('Aruba', 'Aruba'),
        ('Afghanistan', 'Afghanistan'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('\xc5land Islands', '\xc5land Islands'),
        ('Albania', 'Albania'),
        ('Andorra', 'Andorra'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('American Samoa', 'American Samoa'),
        ('Antarctica', 'Antarctica'),
        ('French Southern Territories', 'French Southern Territories'),
        ('Antigua and Barbuda', 'Antigua and Barbuda'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Burundi', 'Burundi'),
        ('Belgium', 'Belgium'),
        ('Benin', 'Benin'),
        ('Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Bangladesh', 'Bangladesh'),
        ('Bulgaria', 'Bulgaria'),
        ('Bahrain', 'Bahrain'),
        ('Bahamas', 'Bahamas'),
        ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
        ('Saint Barth\xe9lemy', 'Saint Barth\xe9lemy'),
        ('Belarus', 'Belarus'),
        ('Belize', 'Belize'),
        ('Bermuda', 'Bermuda'),
        ('Bolivia, Plurinational State of', 'Bolivia, Plurinational State of'),
        ('Brazil', 'Brazil'),
        ('Barbados', 'Barbados'),
        ('Brunei Darussalam', 'Brunei Darussalam'),
        ('Bhutan', 'Bhutan'),
        ('Bouvet Island', 'Bouvet Island'),
        ('Botswana', 'Botswana'),
        ('Central African Republic', 'Central African Republic'),
        ('Canada', 'Canada'),
        ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
        ('Switzerland', 'Switzerland'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ("C\xf4te d'Ivoire", "C\xf4te d'Ivoire"),
        ('Cameroon', 'Cameroon'),
        ('Congo, The Democratic Republic of the', 'Congo, The Democratic Republic of the'),
        ('Congo', 'Congo'),
        ('Cook Islands', 'Cook Islands'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Costa Rica', 'Costa Rica'),
        ('Cuba', 'Cuba'),
        ('Cura\xe7ao', 'Cura\xe7ao'),
        ('Christmas Island', 'Christmas Island'),
        ('Cayman Islands', 'Cayman Islands'),
        ('Cyprus', 'Cyprus'),
        ('Czechia', 'Czechia'),
        ('Germany', 'Germany'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Denmark', 'Denmark'),
        ('Dominican Republic', 'Dominican Republic'),
        ('Algeria', 'Algeria'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('Eritrea', 'Eritrea'),
        ('Western Sahara', 'Western Sahara'),
        ('Spain', 'Spain'),
        ('Estonia', 'Estonia'),
        ('Ethiopia', 'Ethiopia'),
        ('Finland', 'Finland'),
        ('Fiji', 'Fiji'),
        ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
        ('France', 'France'),
        ('Faroe Islands', 'Faroe Islands'),
        ('Micronesia, Federated States of', 'Micronesia, Federated States of'),
        ('Gabon', 'Gabon'),
        ('United Kingdom', 'United Kingdom'),
        ('Georgia', 'Georgia'),
        ('Guernsey', 'Guernsey'),
        ('Ghana', 'Ghana'),
        ('Gibraltar', 'Gibraltar'),
        ('Guinea', 'Guinea'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Gambia', 'Gambia'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Greece', 'Greece'),
        ('Grenada', 'Grenada'),
        ('Greenland', 'Greenland'),
        ('Guatemala', 'Guatemala'),
        ('French Guiana', 'French Guiana'),
        ('Guam', 'Guam'),
        ('Guyana', 'Guyana'),
        ('Hong Kong', 'Hong Kong'),
        ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'),
        ('Honduras', 'Honduras'),
        ('Croatia', 'Croatia'),
        ('Haiti', 'Haiti'),
        ('Hungary', 'Hungary'),
        ('Indonesia', 'Indonesia'),
        ('Isle of Man', 'Isle of Man'),
        ('India', 'India'),
        ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
        ('Ireland', 'Ireland'),
        ('Iran, Islamic Republic of', 'Iran, Islamic Republic of'),
        ('Iraq', 'Iraq'),
        ('Iceland', 'Iceland'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Jamaica', 'Jamaica'),
        ('Jersey', 'Jersey'),
        ('Jordan', 'Jordan'),
        ('Japan', 'Japan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Cambodia', 'Cambodia'),
        ('Kiribati', 'Kiribati'),
        ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
        ('Korea, Republic of', 'Korea, Republic of'),
        ('Kuwait', 'Kuwait'),
        ("Lao People's Democratic Republic", "Lao People's Democratic Republic"),
        ('Lebanon', 'Lebanon'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Saint Lucia', 'Saint Lucia'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Lesotho', 'Lesotho'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Latvia', 'Latvia'),
        ('Macao', 'Macao'),
        ('Saint Martin (French part)', 'Saint Martin (French part)'),
        ('Morocco', 'Morocco'),
        ('Monaco', 'Monaco'),
        ('Moldova, Republic of', 'Moldova, Republic of'),
        ('Madagascar', 'Madagascar'),
        ('Maldives', 'Maldives'),
        ('Mexico', 'Mexico'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Macedonia, Republic of', 'Macedonia, Republic of'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Myanmar', 'Myanmar'),
        ('Montenegro', 'Montenegro'),
        ('Mongolia', 'Mongolia'),
        ('Northern Mariana Islands', 'Northern Mariana Islands'),
        ('Mozambique', 'Mozambique'),
        ('Mauritania', 'Mauritania'),
        ('Montserrat', 'Montserrat'),
        ('Martinique', 'Martinique'),
        ('Mauritius', 'Mauritius'),
        ('Malawi', 'Malawi'),
        ('Malaysia', 'Malaysia'),
        ('Mayotte', 'Mayotte'),
        ('Namibia', 'Namibia'),
        ('New Caledonia', 'New Caledonia'),
        ('Niger', 'Niger'),
        ('Norfolk Island', 'Norfolk Island'),
        ('Nigeria', 'Nigeria'),
        ('Nicaragua', 'Nicaragua'),
        ('Niue', 'Niue'),
        ('Netherlands', 'Netherlands'),
        ('Norway', 'Norway'),
        ('Nepal', 'Nepal'),
        ('Nauru', 'Nauru'),
        ('New Zealand', 'New Zealand'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Panama', 'Panama'),
        ('Pitcairn', 'Pitcairn'),
        ('Peru', 'Peru'),
        ('Philippines', 'Philippines'),
        ('Palau', 'Palau'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Poland', 'Poland'),
        ('Puerto Rico', 'Puerto Rico'),
        ("Korea, Democratic People's Republic of", "Korea, Democratic People's Republic of"),
        ('Portugal', 'Portugal'),
        ('Paraguay', 'Paraguay'),
        ('Palestine, State of', 'Palestine, State of'),
        ('French Polynesia', 'French Polynesia'),
        ('Qatar', 'Qatar'),
        ('R\xe9union', 'R\xe9union'),
        ('Romania', 'Romania'),
        ('Russian Federation', 'Russian Federation'),
        ('Rwanda', 'Rwanda'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Sudan', 'Sudan'),
        ('Senegal', 'Senegal'),
        ('Singapore', 'Singapore'),
        ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
        ('Saint Helena, Ascension and Tristan da Cunha', 'Saint Helena, Ascension and Tristan da Cunha'),
        ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Sierra Leone', 'Sierra Leone'),
        ('El Salvador', 'El Salvador'),
        ('San Marino', 'San Marino'),
        ('Somalia', 'Somalia'),
        ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'),
        ('Serbia', 'Serbia'),
        ('South Sudan', 'South Sudan'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Suriname', 'Suriname'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Sweden', 'Sweden'),
        ('Swaziland', 'Swaziland'),
        ('Sint Maarten (Dutch part)', 'Sint Maarten (Dutch part)'),
        ('Seychelles', 'Seychelles'),
        ('Syrian Arab Republic', 'Syrian Arab Republic'),
        ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
        ('Chad', 'Chad'),
        ('Togo', 'Togo'),
        ('Thailand', 'Thailand'),
        ('Tajikistan', 'Tajikistan'),
        ('Tokelau', 'Tokelau'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Timor-Leste', 'Timor-Leste'),
        ('Tonga', 'Tonga'),
        ('Trinidad and Tobago', 'Trinidad and Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Tuvalu', 'Tuvalu'),
        ('Taiwan, Province of China', 'Taiwan, Province of China'),
        ('Tanzania, United Republic of', 'Tanzania, United Republic of'),
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'),
        ('Uruguay', 'Uruguay'),
        ('United States', 'United States'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
        ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
        ('Venezuela, Bolivarian Republic of', 'Venezuela, Bolivarian Republic of'),
        ('Virgin Islands, British', 'Virgin Islands, British'),
        ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'),
        ('Vietnam', 'Vietnam'),
        ('Vanuatu', 'Vanuatu'),
        ('Wallis and Futuna', 'Wallis and Futuna'),
        ('Samoa', 'Samoa'),
        ('Yemen', 'Yemen'),
        ('South Africa', 'South Africa'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe')
    ]

    territory = models.CharField(max_length=50, choices=COUNTRIES_CHOICES, default='')
    territory_usa = models.CharField(max_length=1000, null=True, blank=True)

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='%(class)s_details')

    def __str__(self):
        return self.order.song_title

    class Meta:
        abstract = True


class OrderProjectBase(Base):
    '''
    base class for all project based classes
    '''
    production_name = models.CharField(max_length=300)
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='order_project_%(class)s')

    class Meta:
        abstract = True


class OrderFilmMaking(OrderProjectBase):
    '''
    the data we need on indie film projects
    '''
    FILM_LENGTH = [
        ('short', 'short film'),
        ('full', 'full length')
    ]
    YES_NO = [
        ('n', 'no'),
        ('y', 'yes')
    ]
    film_length = models.CharField(max_length=10, choices=FILM_LENGTH, default='short')
    film_programming = models.CharField(max_length=2, choices=YES_NO, default='n')
    film_trailer = models.CharField(max_length=2, choices=YES_NO, default='n')
    distribution = models.ManyToManyField(OrderDistributionIndie,
                                          related_name='order_dist_indie')

    def __str__(self):
        return 'indie movie' + self.production_name

    class Meta:
        verbose_name = 'film making project'
        verbose_name_plural = 'film making projects'


class FeaturedBackground(Base):
    '''
    this class should have only 2 options, featured and background on it's field,
    but since this is a multi choice option we need a model.
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'feature or background'
        verbose_name_plural = 'featured or backgrounds'


class OrderProgramming(OrderProjectBase):
    '''
    basic data we need from programming projects
    '''
    distribution = models.ManyToManyField(OrderDistributionProgramming,
                                          related_name='order_dist_programming')

    class Meta:
        verbose_name = 'programming project'
        verbose_name_plural = 'programming projects'


class OrderAdvertising(OrderProjectBase):
    '''
    basic data about advertising projects
    '''
    distribution = models.ManyToManyField(OrderDistributionProgramming,
                                          related_name='order_dist_advertising')

    class Meta:
        verbose_name = 'advertising project'
        verbose_name_plural = 'advertising projects'


class ProjectDetailBase(OrderProjectDetailBase):
    '''
    base class for project details classes
    '''
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

    IS_NON_PROFIT_CHOICES = [
        ('no', 'non profit'),
        ('yes', 'profit')
    ]

    number_uses = models.IntegerField()
    opening_closing = models.BooleanField(default=False)
    featured_background = models.ManyToManyField(FeaturedBackground,
                                                 related_name='programming_project_detail_%(class)s')
    song_version = models.CharField(max_length=20, choices=SONG_VERSION_CHOICES, default=ORIGINAL)

    # start and end point of the song to work on
    start_duration = models.CharField(max_length=8)
    end_duration = models.CharField(max_length=8)
    term = models.CharField(max_length=2,
                            choices=TERM_CHOICES,
                            default=YEAR1)

    release_date = models.DateField()
    budget = models.CharField(max_length=5, choices=BUDGET_CHOICES, default='low')

    synopsis = models.CharField(max_length=1000)
    description = models.TextField()

    is_non_profit = models.CharField(max_length=3, choices=IS_NON_PROFIT_CHOICES, default='no')
    non_profit = models.CharField(max_length=3, choices=NON_PROFIT_CHOICES,
                                  null=True, blank=True)

    comments = models.TextField(null=True, blank=True)

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_details_%(class)s')

    def __str__(self):
        return 'details for project: %(class)s- ' + self.order.song_title

    class Meta:
        abstract = True


class RateUs(Base):
    rate = models.SmallIntegerField(null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_rate_us')


class OrderIndieProjectDetail(ProjectDetailBase):
    '''
    details about the film making project
    '''
    class Meta:
        verbose_name = 'film making project details'
        verbose_name_plural = 'film making projects details'


class OrderProgrammingDetail(ProjectDetailBase):
    '''
    details about the programming project
    '''
    class Meta:
        verbose_name = 'programming project detail'
        verbose_name_plural = 'programming project details'


class OrderAdvertisingDetail(ProjectDetailBase):
    '''
    details about advertising projects
    '''
    class Meta:
        verbose_name = 'advertising project details'
        verbose_name_plural = 'advertising projects details'


class OrderWedding(OrderProjectDetailBase):
    '''
    data about wedding project
    '''
    platform = models.CharField(max_length=1000)
    num_uses = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'wedding project'
        verbose_name_plural = 'wedding projects'


class OrderPersonal(OrderProjectDetailBase):
    '''
    data about personal projects
    '''
    purpose = models.CharField(max_length=1000)
    platform = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'personal project'
        verbose_name_plural = 'personal projects'


def license_path(instance, filename):
    '''
    file will be uploaded to MEDIA_ROOT/user_id/file_name
    :param instance: an instance of this class
    :param filename: the original file name
    :return: the path to the file
    '''
    return 'licenses/user_{0}/{1}/'.format(instance.user.id, filename)


class Order(Base):
    '''
    basic project data
    '''
    SENT = 'sent'
    DONE = 'done'
    ATTENTION = 'attention'
    PAYMENT = 'payment'

    ORDER_CHOICES = (
        (SENT, 'Sent'),
        (ATTENTION, 'Attention'),
        (PAYMENT, 'payment'),
        (DONE, 'Done'),
    )

    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    state = models.CharField(max_length=20,
                             choices=ORDER_CHOICES,
                             default=SENT)

    song = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, blank=True)
    song_title = models.CharField(max_length=200)
    performer_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_done = models.BooleanField(default=False)
    license_pdf = models.FileField(upload_to=license_path, null=True, blank=True)
    supporter = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  limit_choices_to={'is_staff': True},
                                  related_name='supporter')

    project_type = models.ForeignKey(ProjectType, related_name='general_order')

    def __str__(self):
        return str(self.id) + '- ' + str(self.user) + ': ' + self.song_title

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
