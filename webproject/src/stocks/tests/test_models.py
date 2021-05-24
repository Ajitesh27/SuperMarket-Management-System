from django.test import TestCase
from ..models import Product
from accounts.models import User

class ProductModelTest(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        Product.objects.create(name="sugar", description="This is a stock of kakira sugar",
                                quantity=10, unit_price=4000.0, stock_level=10, created_by=User.objects.get(username="admintest"))
        Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, unit_price=5000.0, stock_level=20, created_by=User.objects.get(username="admintest"))

    def test_product_was_created(self):
        sugar = Product.objects.get(name="sugar")
        bread = Product.objects.get(name="bread")

        self.assertEqual(sugar.name, "sugar")
        self.assertEqual(sugar.description, "This is a stock of kakira sugar")

        self.assertEqual(bread.name, "bread")
        self.assertEqual(bread.description, "This is a stock of bread")

    def test_product_object_return_correct_str_rep(self):
        prod = Product.objects.create(name="apple", description="This is a stock of apple",
                                quantity=100, unit_price=2000.0, stock_level=100, created_by=User.objects.get(username="admintest"))
        self.assertEqual(str(prod), 'apple')

    def test_product_name_label(self):
        prod = Product.objects.get(name="sugar")
        field_label = prod._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_product_description_label(self):
        prod = Product.objects.get(name="sugar")
        field_label = prod._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_product_quantity_label(self):
        prod = Product.objects.get(name="sugar")
        field_label = prod._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')

    def test_product_unit_price_label(self):
        prod = Product.objects.get(name="sugar")
        field_label = prod._meta.get_field('unit_price').verbose_name
        self.assertEquals(field_label, 'unit price')

    def test_product_stock_level_label(self):
        prod = Product.objects.get(name="sugar")
        field_label = prod._meta.get_field('stock_level').verbose_name
        self.assertEquals(field_label, 'stock level')

    def test_product_name_max_length(self):
        prod = Product.objects.get(name="sugar")
        max_length = prod._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_product_description_max_length(self):
        prod = Product.objects.get(name="sugar")
        max_length = prod._meta.get_field('description').max_length
        self.assertEquals(max_length, 100)

    def test_product_count(self):
        count = Product.objects.count()
        self.assertEqual(count, 2)