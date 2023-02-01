from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product_category = models.ForeignKey("ProductType", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    cost = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.added_by.username

    def __str__(self):
        return self.product_category.category