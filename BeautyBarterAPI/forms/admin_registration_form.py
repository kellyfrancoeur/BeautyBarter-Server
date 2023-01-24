from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from BeautyBarterAPI.models import Admin

class AdminRegistrationForm(UserCreationForm):
    position = forms.CharField(max_length=500)
    img = forms.CharField(max_length=1000)

    class Meta:
        model = Admin
        fields = ('position', 'img')