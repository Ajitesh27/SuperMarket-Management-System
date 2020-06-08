from django.test import TestCase
from accounts.models import User
from stocks.models import Product
from sales.forms import SalesCreationForm, EditSalesForm

class SalesCreationFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.prod = Product.objects.create(name="bread", description="This is a stock of bread",
                                    quantity=20, unit_price=5000.0, stock_level=20,
                                    created_by=User.objects.get(username="test"))
        self.sale_creater = SalesCreationForm()
        self.sale_creater2 = SalesCreationForm(
            data={
                'name': self.prod.name,
                'item': self.prod.id,
                'quantity': 4,
                'unit_price': self.prod.unit_price,
                'total_amount': self.prod.unit_price * 4,
                'sold_by': self.test.id
            }
        )

    def test_sale_name_field_label(self):
        self.assertFalse(self.sale_creater.fields['name'].label is None)
        self.assertFalse(self.sale_creater.fields['name'].label == 'name')

    def test_sale_item_field_label(self):
        self.assertFalse(self.sale_creater.fields['item'].label is None)
        self.assertFalse(self.sale_creater.fields['item'].label == 'item')

    def test_sale_quantity_field_label(self):
        self.assertFalse(self.sale_creater.fields['quantity'].label is None)
        self.assertFalse(self.sale_creater.fields['quantity'].label == 'quantity')

    def test_sale_unit_price_field_label(self):
        self.assertFalse(self.sale_creater.fields['unit_price'].label is None)
        self.assertFalse(self.sale_creater.fields['unit_price'].label == 'unit price')

    def test_sale_total_amount_field_label(self):
        self.assertFalse(self.sale_creater.fields['total_amount'].label is None)
        self.assertFalse(self.sale_creater.fields['total_amount'].label == 'total amount')

    def test_form_is_valid(self):
        self.assertTrue(self.sale_creater2.is_valid())

    def test_form_is_not_valid(self):
        self.assertFalse(self.sale_creater.is_valid())

class EditSalesFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.prod = Product.objects.create(name="bread", description="This is a stock of bread",
                                    quantity=20, unit_price=5000.0, stock_level=20,
                                    created_by=User.objects.get(username="test"))
        self.sale_creater = EditSalesForm()
        self.sale_creater2 = EditSalesForm(
            data={
                'name': self.prod.name,
                'item': self.prod.id,
                'quantity': 4,
                'unit_price': self.prod.unit_price,
                'total_amount': self.prod.unit_price * 4,
                'sold_by': self.test.id
            }
        )

    def test_sale_item_field_label(self):
        self.assertFalse(self.sale_creater.fields['item'].label is None)
        self.assertFalse(self.sale_creater.fields['item'].label == 'item')

    def test_sale_quantity_field_label(self):
        self.assertFalse(self.sale_creater.fields['quantity'].label is None)
        self.assertFalse(self.sale_creater.fields['quantity'].label == 'quantity')

    def test_form_is_valid(self):
        self.assertTrue(self.sale_creater2.is_valid())

    def test_form_is_not_valid(self):
        self.assertFalse(self.sale_creater.is_valid())
