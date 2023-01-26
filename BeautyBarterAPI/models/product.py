from django.db import models

class Product(models.Model):

    member = models.ForeignKey("Member", null=True, blank=True, on_delete=models.CASCADE)
    admin = models.ForeignKey("Admin", null=True, blank=True, on_delete=models.CASCADE)
    product_category = models.ForeignKey("ProductType", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    cost = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.member.username

    def __str__(self):
        return self.admin.username

    def __str__(self):
        return self.product_category.category