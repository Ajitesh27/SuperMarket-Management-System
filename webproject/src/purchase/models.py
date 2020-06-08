from django.db import models
from accounts.models import User

class Purchase(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=100,unique=True)
    quantity = models.PositiveIntegerField()
    cost_price = models.FloatField(verbose_name='cost price')
    current_stock_level = models.PositiveIntegerField(verbose_name='current stock level')
    total_stock_level = models.PositiveIntegerField(verbose_name='total stock level')
    supplier_tel = models.CharField(max_length=13,unique=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of this Purchase."""
        return self.name
