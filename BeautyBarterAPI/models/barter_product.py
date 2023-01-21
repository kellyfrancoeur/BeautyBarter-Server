from django.db import models

class BarterProduct(models.Model):

    barter = models.ForeignKey("Barter", null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name