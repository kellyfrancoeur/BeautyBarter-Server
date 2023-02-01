from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey("Profession", null=True, blank=True, on_delete=models.CASCADE)
    service = models.CharField(max_length=500)
    cost = models.IntegerField(null=True, blank=True)
    per = models.CharField(max_length=100)

    def __str__(self):
        return self.created_by.username

    def __str__(self):
        return self.category.profession