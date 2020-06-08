from django import forms
from sales.models import Sales

class SalesCreationForm(forms.ModelForm):
    """
    A form for adding new sales with all required field
    """
    class Meta:
        model = Sales
        fields = ('name','item', 'quantity', 'unit_price', 'total_amount', 'sold_by')

    def save(self, commit=True):
        """
        Save form data to database
        """
        sale = super(SalesCreationForm, self).save(commit=False)

        if commit:
            sale.name = self.cleaned_data.get('name')
            sale.unit_price = self.cleaned_data.get('unit_price')
            sale.total_amount = self.cleaned_data.get('total_amount')
            sale.sold_by = self.cleaned_data.get('sold_by')
            sale.save()
        return sale

class EditSalesForm(forms.ModelForm):
    """
    A form for editing sales record with all required field
    """
    class Meta:
        model = Sales
        fields = ['item', 'quantity']
