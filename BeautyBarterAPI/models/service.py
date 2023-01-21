from django.db import models

class Service(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='member')
    admin = models.ForeignKey("Admin", null=True, blank=True, on_delete=models.CASCADE, related_name='admin')
    category = models.ForeignKey("Profession", null=True, blank=True, on_delete=models.CASCADE, related_name='product_category')
    service = models.CharField(max_length=500)
    cost = models.IntegerField(null=True, blank=True)
    per = models.CharField(max_length=100)

    def __str__(self):
        return self.member.username

    def __str__(self):
        return self.admin.username

    def __str__(self):
        return self.category.profession