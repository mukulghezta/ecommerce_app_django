from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import Customer


class Order(models.Model):
    order_id        = models.AutoField(primary_key=True)
    user            = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    course          = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    amount          = models.DecimalField(max_digits=6, decimal_places=2)
    gst_amount      = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    final_amount    = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    order_date      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


class CancelledOrder(models.Model):
    order_id                = models.ForeignKey(Order, primary_key=True, on_delete=models.CASCADE)
    user                    = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    amount                  = models.DecimalField(max_digits=6, decimal_places=2)
    gst_amount              = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    final_amount            = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    order_date              = models.DateTimeField(blank=True, null=True)
    cancelled_order_date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


class CancelledApproval(models.Model):
    order_id             = models.ForeignKey(CancelledOrder, primary_key=True, on_delete=models.CASCADE)
    user                 = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    amount               = models.DecimalField(max_digits=6, decimal_places=2)
    gst_amount           = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    final_amount         = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    order_date           = models.DateTimeField(blank=True, null=True)
    cancelled_order_date = models.DateTimeField(blank=True, null=True)
    date_diff            = models.IntegerField()
    refund_amount        = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return str(self.order_id)


class Email(models.Model):
    email_id         = models.IntegerField(primary_key=True)
    email_type       = models.CharField(max_length=50)
    email_subject    = models.CharField(max_length=50, null=True)
    email_body       = models.TextField(null=True)
    email_sender     = models.CharField(max_length=50, null=True, blank=True)
    email_recipients = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.email_type


class Discount(models.Model):
    discount_id      = models.IntegerField(primary_key=True)
    discount_start   = models.IntegerField()
    discount_end     = models.IntegerField()
    discount_percent = models.DecimalField(max_digits=6, decimal_places=2)
    

    def __str__(self):
        return str(self.discount_id)

class GST(models.Model):
    gst = models.DecimalField(max_digits=6  , decimal_places=2)

    def __str__(self):
        return str(self.gst)


