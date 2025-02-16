from django.db import models
from apps.users.models import User
from apps.products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('PROCESSING', 'В обработке'),
        ('SHIPPED', 'Отправлен'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменён'),
    ]

    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} pcs'

    def total_price(self):
        return self.quantity * self.price
