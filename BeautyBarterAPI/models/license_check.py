from django.db import models

class LicenseCheck(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='member')
    admin = models.ForeignKey("Admin", null=True, blank=True, on_delete=models.CASCADE, related_name='admin')
    license_state = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='license_state')
    license_number = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='license_number')
    date_requested = models.DateTimeField()

    def __str__(self):
        return self.member.username

    def __str__(self):
        return self.admin.full_name
    
    def __str__(self):
        return self.license_state.license_state

    def __str__(self):
        return self.license_number.license_number