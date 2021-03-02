from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import Customer


class Order(models.Model):
    order_id       = models.AutoField(primary_key=True)
    user           = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    course         = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    # product_seller = models.CharField(max_length=100)
    amount         = models.IntegerField(default=0)
    order_date     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


class CancelledOrder(models.Model):
    order_id             = models.ForeignKey(Order, primary_key=True, on_delete=models.CASCADE)
    user                 = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    # product_seller = models.CharField(max_length=100)
    amount               = models.IntegerField(default=0)
    cancelled_order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


class CancelledApproval(models.Model):
    order_id             = models.ForeignKey(CancelledOrder, primary_key=True, on_delete=models.CASCADE)
    user                 = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    amount               = models.IntegerField(default=0)
    cancelled_order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)



