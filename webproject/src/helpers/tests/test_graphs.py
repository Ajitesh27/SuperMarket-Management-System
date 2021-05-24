from django.test import TestCase
from django.urls import reverse_lazy
from accounts.models import User, Role
from stocks.models import Product
from sales.models import Sales
from expenses.models import Expenses, ExpenseCategory
from purchase.models import Purchase

class GraphsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Role.objects.create(name="Manager", description="This is a manager role")
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        ExpenseCategory.objects.create(name="purchases",
                                description="This is an expense on cost of purchasing new stocks",
                                created_by=User.objects.get(username="admintest"))
        Expenses.objects.create(category=ExpenseCategory.objects.get(name='purchases'),
                                description="This is the cost of buying 10 bags of sugar",
                                amount=700000,
                                created_by=User.objects.get(username="admintest"))
        Expenses.objects.create(category=ExpenseCategory.objects.get(name='purchases'),
                                description="This is the cost of buying 5 boxes of soap",
                                amount=500000,
                                created_by=User.objects.get(username="admintest"))
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

    def test_index_url(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)

    def test_roles_graph_url(self):
        response = self.client.get(reverse_lazy('roles_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.json()), dict)
        self.assertEqual(response.json()['series'][0]['name'],'Roles')

    def test_stocks_graph_url(self):
        response = self.client.get(reverse_lazy('stocks_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.json()), dict)
        self.assertEqual(response.json()['series'][0]['name'],'Products')

    def test_sales_graph_url(self):
        response = self.client.get(reverse_lazy('sales_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.json()), dict)
        self.assertEqual(response.json()['series'][0]['name'],'Products')

    def test_expenses_graph_url(self):
        response = self.client.get(reverse_lazy('expenses_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.json()), dict)
        self.assertEqual(response.json()['series'][0]['name'],'Expenses')
