from django.db import models
from accounts.models import User

class Product(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=100,unique=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField()
    stock_level = models.PositiveIntegerField()
    created_by_id=models.PositiveIntegerField(default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of this Product."""
        return self.name
