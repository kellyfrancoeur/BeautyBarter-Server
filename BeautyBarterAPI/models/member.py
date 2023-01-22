from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_member')
    profession = models.ForeignKey("Profession", null=True, blank=True, on_delete=models.CASCADE, related_name='member_profession')
    license_state= models.ForeignKey("LicenseState", null=True, blank=True, on_delete=models.CASCADE, related_name='member_license_state')
    license_number = models.IntegerField(null=True, blank=True)
    link_to_site = models.CharField(max_length=500)
    about = models.CharField(max_length=1000)
    interested_in = models.CharField(max_length=500)
    willing_to_trade = models.CharField(max_length=500)
    img = models.CharField(max_length=1000)
    portfolio_img = models.CharField(max_length=1000)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'

    @property
    def email(self):
        return f'{self.user.email}'