from django.db import models
from accounts.models import SalesExecutive

class Product(models.Model):
    product_id      = models.IntegerField(primary_key=True)
    product_name    = models.CharField(max_length=100)
    product_price   = models.DecimalField(max_digits=6, decimal_places=2)
    product_seller  = models.ForeignKey(SalesExecutive, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name

