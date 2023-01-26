from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_admin')
    position = models.CharField(max_length=250)
    admin_img = models.ImageField(upload_to='images/', null=True, blank=True)


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'

    @property
    def email(self):
        return f'{self.user.email}'