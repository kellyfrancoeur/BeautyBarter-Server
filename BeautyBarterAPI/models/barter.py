from django.db import models

class Barter(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE)
    service_requested = models.ForeignKey("Service", null=True, blank=True, on_delete=models.CASCADE, related_name='requested_service')
    service_offered = models.ForeignKey("Service", null=True, blank=True, on_delete=models.CASCADE, related_name='offered_service')
    date_posted = models.DateTimeField()
    requested_details = models.TextField(blank=True)
    offered_details = models.TextField(blank=True)
    includes_product = models.BooleanField(default=False)
    products = models.ManyToManyField("Product", through = "BarterProduct")

    def __str__(self):
        return self.member.username
    
    def __str__(self):
        return self.service_requested.service
    
    def __str__(self):
        return self.service_offered.service
    