from django import forms
from .models import Purchase

class PurchaseCreationForm(forms.ModelForm):
    """
    A form for adding new purchase with all required field
    """
    class Meta:
        model = Purchase
        fields = ('name', 'description', 'quantity', 'cost_price', 'current_stock_level',
                'total_stock_level', 'supplier_tel', 'created_by')

class EditPurchaseForm(forms.ModelForm):
    """
    A form for editing existing purchase with all required field
    """
    class Meta:
        model = Purchase
        fields = ['name', 'description', 'quantity', 'cost_price','current_stock_level',
                'total_stock_level', 'supplier_tel',]
        exclude = ['created_by']
