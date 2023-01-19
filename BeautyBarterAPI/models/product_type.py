from django.db import models

class ProductType(models.Model):

    category = models.ForeignKey("Profession", null=True, blank=True, on_delete=models.CASCADE, related_name='product_category')
    type = models.CharField(max_length=150)

    def __str__(self):
        return self.category.profession