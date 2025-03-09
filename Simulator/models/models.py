from django.db import models

# Create your models here.
from django.db import models

# TODO: Before adding to DB check that their username is unique
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="username", max_length=64)
    password = models.CharField(verbose_name="password", max_length=64)
    equity = models.DecimalField(verbose_name="equity", max_digits=10, decimal_places=2)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField(verbose_name="price")
    quantity = models.IntegerField(verbose_name='quantity')
    user = models.ForeignKey(
        Users,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(verbose_name = "timestamp", auto_now_add=True)
    
class PriceHistory(models.Model):
    price = models.IntegerField(verbose_name="price")
    created_time = models.DateTimeField(verbose_name = "timestamp", auto_now_add=True)

class Positions(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField(verbose_name="price")
    quantity = models.IntegerField(verbose_name='quantity')
    user = models.ForeignKey(
        Users,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(verbose_name = "timestamp", auto_now_add=True)