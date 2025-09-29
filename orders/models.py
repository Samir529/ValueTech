# from django.db import models
# from django.contrib.auth.models import User
# from store.models import Product
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"
#
#     def total_price(self):
#         return sum(item.subtotal() for item in self.items.all())
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"
#
#     def subtotal(self):
#         return self.product.price * self.quantity
#

from django.db import models
from store.models import Product


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("cod_inside", "Cash On Delivery (Inside Dhaka)"),
        ("cod_outside", "Cash On Delivery (Outside Dhaka)"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    town_city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="Bangladesh")
    district = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity
