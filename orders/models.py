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
