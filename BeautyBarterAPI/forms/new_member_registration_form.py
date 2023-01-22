from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewMemberRegistrationForm(UserCreationForm):
    profession = forms.ChoiceField(choices=[
        ('cosmetologist', 'Cosmetologist'),
        ('barber', 'Barber'),
        ('nail_technician', 'Nail Technician'),
        ('aesthetician', 'Aesthetician'),
        ('massage_therapist', 'Massage Therapist'),
        ('lash_technician', 'Lash Technician'),
        ('tattoo_artist', 'Tattoo Artist')
        ])
    license_state = forms.ChoiceField(choices=[
        ('al', 'AL'), 
        ('ak', 'AK'),
        ('az', 'AZ'),
        ('ar', 'AR'),
        ('ca', 'CA'),
        ('co', 'CO'),
        ('ct', 'CT'),
        ('de', 'DE'),
        ('dc', 'DC'),
        ('fl', 'FL'),
        ('ga', 'GA'),
        ('hi', 'HI'),
        ('id', 'ID'),
        ('il', 'IL'),
        ('in', 'IN'),
        ('ia', 'IA'),
        ('ks', 'KS'),
        ('ky', 'KY'),
        ('la', 'LA'),
        ('me', 'ME'),
        ('md', 'MD'),
        ('ma', 'MA'),
        ('mi', 'MI'),
        ('mn', 'MN'),
        ('ms', 'MS'),
        ('mo', 'MO'),
        ('mt', 'MT'),
        ('ne', 'NE'),
        ('nv', 'NV'),
        ('nh', 'NH'),
        ('nj', 'NJ'),
        ('nm', 'NM'),
        ('ny', 'NY'),
        ('nc', 'NC'),
        ('nd', 'ND'),
        ('oh', 'OH'),
        ('ok', 'OK'),
        ('or', 'OR'),
        ('pa', 'PA'),
        ('pr', 'PR'),
        ('ri', 'RI'),
        ('sc', 'SC'),
        ('sd', 'SD'),
        ('tn', 'TN'),
        ('tx', 'TX'),
        ('ut', 'UT'),
        ('vt', 'VT'),
        ('vi', 'VI'),
        ('va', 'VA'),
        ('wa', 'WA'),
        ('wv', 'WV'),
        ('wi', 'WI'),
        ('wy', 'WY')
        ])
    license_number = forms.IntegerField()
    link_to_site = forms.CharField(max_length=500)
    about = forms.CharField(max_length=1000)
    interested_in = forms.CharField(max_length=500)
    willing_to_trade = forms.CharField(max_length=500)
    img = forms.CharField(max_length=1000)
    portfolio_img = forms.CharField(max_length=1000)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profession', 'license_state', 'license_number', 'link_to_site', 'about', 'interested_in', 'willing_to_trade', 'img', 'porfolio_img')