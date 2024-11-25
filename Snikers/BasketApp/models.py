from django.db import models
from ProductApp.models import Product
from django.contrib.auth.models import User


class UserBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
