from django import forms
from .models import Product

class ProductCreationForm(forms.ModelForm):
    """
    A form for creating new product with all required field
    """
    class Meta:
        model = Product
        fields = ('name', 'description', 'quantity', 'unit_price', 'stock_level', 'created_by_id')

class EditProductForm(forms.ModelForm):
    """
    A form for editing existing product with all required field
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'unit_price','stock_level']
        exclude = ['created_by_id']
