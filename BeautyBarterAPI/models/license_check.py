from django.db import models

class LicenseCheck(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='new_member')
    approved_by = models.ForeignKey("Admin", null=True, blank=True, on_delete=models.CASCADE)
    license_state = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='new_member_license_state')
    license_number = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='new_member_license_number')
    date_requested = models.DateTimeField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.member.username

    def __str__(self):
        return self.approved_by.username
    
    def __str__(self):
        return self.license_state.license_state

    def __str__(self):
        return self.license_number.license_number