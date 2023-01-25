from django.db import models

class MemberPortfolioImages(models.Model):

    image = models.ImageField(upload_to='images/', null=True, blank=True)