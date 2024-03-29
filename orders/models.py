from django.db import models
from products.models import Products
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    # product-->foreign key, qty, cart_total, user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart_qty = models.IntegerField(default=0)
    cart_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Orders(models.Model):
    # take refercne from order-summmary
    ORDER_STATUS = [("PENDING","PENDING"), ("DELIVERED", "DELIVERED"), ("ON_THE_WAY", "ON_THE_WAY"),("CANCELLED", "CANCELLED")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.JSONField()
    total = models.FloatField(default=0)
    shipping_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    additional_info = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, default="COD")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PENDING")
    shipping_type = models.CharField(max_length=20, default="SELF_PICKUP")
    discount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk