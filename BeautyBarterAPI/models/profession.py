from django.db import models

class Profession(models.Model):

    profession = models.CharField(max_length=100)
    admin = models.ForeignKey("Admin", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.username