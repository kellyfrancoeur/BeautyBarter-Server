from django.db import models

class LicenseState(models.Model):

    state = models.CharField(max_length=2)