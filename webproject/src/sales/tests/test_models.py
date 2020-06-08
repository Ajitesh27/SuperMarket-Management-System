from django.test import TestCase
from sales.models import Sales
from accounts.models import User
from stocks.models import Product

class SalesModelTest(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        prod = Product.objects.create(name="sugar", description="This is a stock of sugar",
                                quantity=20, unit_price=3000.0, stock_level=20,
                                created_by=User.objects.get(username="admintest"))
        prod2 = Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, unit_price=5000.0, stock_level=20,
                                created_by=User.objects.get(username="admintest"))
        Sales.objects.create(name=prod.name,
                            item=prod,
                            quantity=5, unit_price=prod.unit_price, total_amount=prod.unit_price * 5,
                            sold_by=User.objects.get(username="admintest"))
        Sales.objects.create(name=prod2.name,
                            item=prod2,
                            quantity=2, unit_price=prod2.unit_price, total_amount=prod2.unit_price * 2,
                            sold_by=User.objects.get(username="admintest"))

    def test_sales_was_created(self):
        sugar = Sales.objects.get(name="sugar")
        bread = Sales.objects.get(name="bread")

        self.assertEqual(sugar.unit_price, 3000.0)
        self.assertEqual(sugar.quantity, 5)

        self.assertEqual(bread.unit_price, 5000.0)
        self.assertEqual(bread.quantity, 2)

    def test_sales_object_return_correct_str_rep(self):
        prod1 = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="admintest"))
        sale = Sales.objects.create(name=prod1.name,
                                    item=prod1,
                                    quantity=10, unit_price=2000.0, total_amount=4000.0,
                                    sold_by=User.objects.get(username="admintest"))
        self.assertEqual(str(sale), 'books')

    def test_sales_name_label(self):
        sale = Sales.objects.get(name="sugar")
        field_label = sale._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_sales_item_label(self):
        sale = Sales.objects.get(name="sugar")
        field_label = sale._meta.get_field('item').verbose_name
        self.assertEquals(field_label, 'item')

    def test_sales_status_label(self):
        sale = Sales.objects.get(name="sugar")
        field_label = sale._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_sales_quantity_label(self):
        sale = Sales.objects.get(name="sugar")
        field_label = sale._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')

    def test_sales_unit_price_label(self):
        sale = Sales.objects.get(name="sugar")
        field_label = sale._meta.get_field('unit_price').verbose_name
        self.assertEquals(field_label, 'unit price')

    def test_sales_total_amount_label(self):
        sale = Sales.objects.get(name="sugar")
        field_label = sale._meta.get_field('total_amount').verbose_name
        self.assertEquals(field_label, 'total amount')

    def test_sales_name_max_length(self):
        sale = Sales.objects.get(name="sugar")
        max_length = sale._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_sales_status_max_length(self):
        sale = Sales.objects.get(name="sugar")
        max_length = sale._meta.get_field('status').max_length
        self.assertEquals(max_length, 50)

    def test_sales_count(self):
        count = Sales.objects.count()
        self.assertEqual(count, 2)
