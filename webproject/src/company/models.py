from django.db import models
from accounts.models import User

class Company(models.Model):
    logo = models.ImageField(upload_to='images/', default=False)
    name = models.CharField(max_length=50,unique=True)
    address = models.TextField(max_length=100,unique=True)
    company_tel = models.CharField(max_length=13,unique=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of this company."""
        return self.name
