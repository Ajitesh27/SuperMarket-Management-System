from django.test import TestCase
from accounts.models import User
from ..forms import PurchaseCreationForm, EditPurchaseForm

class PurchaseCreationFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.purch_creater = PurchaseCreationForm()
        self.purch_creater2 = PurchaseCreationForm(
            data={
                'name': 'sugar',
                'description': 'This is a stock of kakira sugar',
                'quantity': 10,
                'cost_price': 3000.0,
                'current_stock_level': 10,
                'total_stock_level': 20,
                'supplier_tel': '256710000000',
                'created_by': self.test.id
            }
        )

    def test_purchase_name_field_label(self):
        self.assertFalse(self.purch_creater.fields['name'].label is None)
        self.assertFalse(self.purch_creater.fields['name'].label == 'name')

    def test_purchase_description_field_label(self):
        self.assertFalse(self.purch_creater.fields['description'].label is None)
        self.assertFalse(self.purch_creater.fields['description'].label == 'description')

    def test_purchase_quantity_field_label(self):
        self.assertFalse(self.purch_creater.fields['quantity'].label is None)
        self.assertFalse(self.purch_creater.fields['quantity'].label == 'quantity')

    def test_purchase_cost_price_field_label(self):
        self.assertFalse(self.purch_creater.fields['cost_price'].label is None)
        self.assertFalse(self.purch_creater.fields['cost_price'].label == 'cost_price')

    def test_purchase_current_stock_level_field_label(self):
        self.assertFalse(self.purch_creater.fields['current_stock_level'].label is None)
        self.assertFalse(self.purch_creater.fields['current_stock_level'].label == 'current_stock_level')

    def test_purchase_total_stock_level_field_label(self):
        self.assertFalse(self.purch_creater.fields['total_stock_level'].label is None)
        self.assertFalse(self.purch_creater.fields['total_stock_level'].label == 'total_stock_level')

    def test_purchase_supplier_tel_field_label(self):
        self.assertFalse(self.purch_creater.fields['supplier_tel'].label is None)
        self.assertFalse(self.purch_creater.fields['supplier_tel'].label == 'supplier_tel')

    def test_form_is_valid(self):
        self.assertTrue(self.purch_creater2.is_valid())

    def test_form_is_not_valid(self):
        self.assertFalse(self.purch_creater.is_valid())

class EditPurchaseFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.purch_creater = EditPurchaseForm()
        self.purch_creater2 = EditPurchaseForm(
            data={
                'name': 'sugar',
                'description': 'This is a stock of kakira sugar',
                'quantity': 10,
                'cost_price': 4000.0,
                'current_stock_level': 10,
                'total_stock_level': 20,
                'supplier_tel': '256710000001',
                'created_by': self.test.id
            }
        )

    def test_purchase_name_field_label(self):
        self.assertFalse(self.purch_creater.fields['name'].label is None)
        self.assertFalse(self.purch_creater.fields['name'].label == 'name')

    def test_purchase_description_field_label(self):
        self.assertFalse(self.purch_creater.fields['description'].label is None)
        self.assertFalse(self.purch_creater.fields['description'].label == 'description')

    def test_purchase_quantity_field_label(self):
        self.assertFalse(self.purch_creater.fields['quantity'].label is None)
        self.assertFalse(self.purch_creater.fields['quantity'].label == 'quantity')

    def test_purchase_cost_price_field_label(self):
        self.assertFalse(self.purch_creater.fields['cost_price'].label is None)
        self.assertFalse(self.purch_creater.fields['cost_price'].label == 'cost_price')

    def test_purchase_current_stock_level_field_label(self):
        self.assertFalse(self.purch_creater.fields['current_stock_level'].label is None)
        self.assertFalse(self.purch_creater.fields['current_stock_level'].label == 'current_stock_level')

    def test_purchase_total_stock_level_field_label(self):
        self.assertFalse(self.purch_creater.fields['total_stock_level'].label is None)
        self.assertFalse(self.purch_creater.fields['total_stock_level'].label == 'total_stock_level')

    def test_purchase_supplier_tel_field_label(self):
        self.assertFalse(self.purch_creater.fields['supplier_tel'].label is None)
        self.assertFalse(self.purch_creater.fields['supplier_tel'].label == 'supplier_tel')

    def test_form_is_valid(self):
        self.assertTrue(self.purch_creater2.is_valid())

    def test_form_is_not_valid(self):
        self.assertFalse(self.purch_creater.is_valid())
