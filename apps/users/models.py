from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.products.models import Product


class User(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email 

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart of {self.user.username}'

    @property
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.product.name} - {self.quantity} pcs'

    def total_price(self):
        return self.quantity * self.product.price

