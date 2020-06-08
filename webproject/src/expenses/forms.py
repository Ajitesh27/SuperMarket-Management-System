from django import forms
from expenses.models import ExpenseCategory, Expenses

class CategoryCreationForm(forms.ModelForm):
    """
    A form for adding new expense category with all required field
    """
    class Meta:
        model = ExpenseCategory
        fields = ('name', 'description', 'created_by')

class EditCategoryForm(forms.ModelForm):
    """
    A form for editing existing category with all required field
    """
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        exclude = ['created_by']

class ExpenseCreationForm(forms.ModelForm):
    """
    A form for adding new expense with all required field
    """
    class Meta:
        model = Expenses
        fields = ('category', 'description', 'amount', 'created_by')

class EditExpenseForm(forms.ModelForm):
    """
    A form for editing existing expense with all required field
    """
    class Meta:
        model = Expenses
        fields = ['description', 'amount']
        exclude = ['category', 'created_by']
