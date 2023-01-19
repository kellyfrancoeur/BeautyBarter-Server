from django.db import models

class Barter(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='member')
    service_requested = models.ForeignKey("Service", null=True, blank=True, on_delete=models.CASCADE, related_name='requested_service')
    service_offered = models.ForeignKey("Service", null=True, blank=True, on_delete=models.CASCADE, related_name='offered_service')
    date_posted = models.DateTimeField()
    requested_details = models.CharField(max_length=1000)
    offered_details = models.CharField(max_length=1000)
    includes_product = models.BooleanField()