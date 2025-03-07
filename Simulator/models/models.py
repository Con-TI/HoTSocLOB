from django.db import models

# Create your models here.
from django.db import models
from enum import Enum

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="username", max_length=64)
    password = models.CharField(verbose_name="password", max_length=64)
    equity = models.DecimalField(verbose_name="equity", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Orders(models.Model):
    class OrderStatus(models.TextChoices, Enum):
        BUY = 1
        SELL = 2
    
    order_id = models.AutoField(primary_key=True)
    price = models.DecimalField(verbose_name="price",max_digits=10, decimal_places=2)
    ordertype = models.CharField(verbose_name = "order_type", choices = OrderStatus.choices, max_length = 64)
    quantity = models.IntegerField(verbose_name='quantity')
    user = models.ForeignKey(
        Users,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(verbose_name = "timestamp", auto_now_add=True)
    def __str__(self):
        return f"Order {self.order_id} for {self.user.name}"

