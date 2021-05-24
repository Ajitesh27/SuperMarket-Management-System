from django import forms
from .models import Company

class CompanyCreationForm(forms.ModelForm):
    """
    A form for adding new company with all required field
    """
    class Meta:
        model = Company
        fields = ('logo', 'name', 'address', 'company_tel', 'created_by')

class EditCompanyForm(forms.ModelForm):
    """
    A form for editing existing company with all required field
    """
    class Meta:
        model = Company
        fields = ['logo', 'name', 'address', 'company_tel',]
        exclude = ['created_by']
