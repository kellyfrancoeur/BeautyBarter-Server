from django.db import models
from datetime import date

class PotentialBarter(models.Model):

    barter = models.ForeignKey("Barter", null=True, blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField()

    def __str__(self):
        return self.member.username

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.date_accepted.date() - today
        days_till_stripped = str(days_till).split(",", 1)[0]
        return days_till_stripped

    @property
    def Is_Past(self):
        today = date.today()
        if self.date_accepted.date() < today:
            potential_barter = "Completed"
        else:
            potential_barter = "Upcoming"
        return potential_barter
