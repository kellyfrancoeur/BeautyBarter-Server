from django.db import models

class Product(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE, related_name='member')
    admin = models.ForeignKey("Admin", null=True, blank=True, on_delete=models.CASCADE, related_name='admin')
    product_category = models.ForeignKey("ProductType", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    instructions = models.CharField(max_length=1000)
    cost = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.member.full_name

    def __str__(self):
        return self.admin.full_name

    def __str__(self):
        return self.product_category.category