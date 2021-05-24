from django.db import models
from accounts.models import User

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=100,unique=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of this expenses category."""
        return self.name

class Expenses(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=100,unique=True)
    amount = models.FloatField(verbose_name='amount')
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of this expense."""
        return self.description
