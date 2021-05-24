from django.test import TestCase
from ..models import Purchase
from accounts.models import User

class PurchaseModelTest(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        Purchase.objects.create(name="sugar",
                                description="This is a stock of kakira sugar",
                                quantity=10,
                                cost_price=4000.0,
                                current_stock_level=10,
                                total_stock_level=20,
                                supplier_tel='256700000000',
                                created_by=User.objects.get(username="admintest"))
        Purchase.objects.create(name="bread",
                                description="This is a stock of bread",
                                quantity=20,
                                cost_price=5000.0,
                                current_stock_level=20,
                                total_stock_level=40,
                                supplier_tel='256710000000',
                                created_by=User.objects.get(username="admintest"))

    def test_purchase_was_created(self):
        sugar = Purchase.objects.get(name="sugar")
        bread = Purchase.objects.get(name="bread")

        self.assertEqual(sugar.name, "sugar")
        self.assertEqual(sugar.description, "This is a stock of kakira sugar")

        self.assertEqual(bread.name, "bread")
        self.assertEqual(bread.description, "This is a stock of bread")

    def test_purchase_object_return_correct_str_rep(self):
        purch = Purchase.objects.create(name="apple", description="This is a stock of apple",
                                quantity=100, cost_price=2000.0, current_stock_level=100,
                                total_stock_level=200, supplier_tel='256720000000',
                                created_by=User.objects.get(username="admintest"))
        self.assertEqual(str(purch), 'apple')

    def test_purchase_name_label(self):
        purch = Purchase.objects.get(name="sugar")
        field_label = purch._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_purchase_description_label(self):
        purch = Purchase.objects.get(name="sugar")
        field_label = purch._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_purchase_quantity_label(self):
        purch = Purchase.objects.get(name="sugar")
        field_label = purch._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')

    def test_purchase_unit_price_label(self):
        purch = Purchase.objects.get(name="sugar")
        field_label = purch._meta.get_field('cost_price').verbose_name
        self.assertEquals(field_label, 'cost price')

    def test_purchase_current_stock_level_label(self):
        purch = Purchase.objects.get(name="sugar")
        field_label = purch._meta.get_field('current_stock_level').verbose_name
        self.assertEquals(field_label, 'current stock level')

    def test_purchase_total_stock_level_label(self):
        purch = Purchase.objects.get(name="sugar")
        field_label = purch._meta.get_field('total_stock_level').verbose_name
        self.assertEquals(field_label, 'total stock level')

    def test_purchase_name_max_length(self):
        purch = Purchase.objects.get(name="sugar")
        max_length = purch._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_purchase_description_max_length(self):
        purch = Purchase.objects.get(name="sugar")
        max_length = purch._meta.get_field('description').max_length
        self.assertEquals(max_length, 100)

    def test_purchase_supplier_tel_max_length(self):
        purch = Purchase.objects.get(name="sugar")
        max_length = purch._meta.get_field('supplier_tel').max_length
        self.assertEquals(max_length, 13)

    def test_purchase_count(self):
        count = Purchase.objects.count()
        self.assertEqual(count, 2)
