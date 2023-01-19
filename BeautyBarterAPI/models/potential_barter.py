from django.db import models

class PotentialBarter(models.Model):

    barter = models.ForeignKey("Barter", null=True, blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE)
    accepted = models.BooleanField()
    date_accepted = models.DateTimeField()

    def __str__(self):
        return self.member.full_name
