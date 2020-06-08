from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.models import User, Role
from stocks.models import Product
from sales.models import Sales
from expenses.models import ExpenseCategory, Expenses
from purchase.models import Purchase

class SearchUserViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
        role = Role.objects.create(name="Manager", description="This is a test role")
        self.test.save()
        role.save()
        self.test2.save()
        self.username = 'test'
        self.password = '1234@test'

    def test_search_user_view(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('search_user'), data={'q':self.test.username})
        self.assertEqual(response.status_code, 200)

class AccountListViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
        role = Role.objects.create(name="Manager", description="This is a test role")
        self.test.save()
        role.save()
        self.test2.save()
        self.username = 'test'
        self.password = '1234@test'

    def test_account_list_view(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('accounts'))
        self.assertEqual(response.status_code, 200)

class SearchSalesViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.prods = Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=10, unit_price=4500.0, stock_level=10,
                                created_by=User.objects.get(username="test"))
        self.sale = Sales.objects.create(name=self.prod.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.sales = Sales.objects.create(name=self.prods.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.test.save()
        self.role.save()
        self.username = 'test'
        self.password = '1234@test'

    def test_search_sales_view(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('search_sale'), data={'q': self.sale.name})
        self.assertEqual(response.status_code, 200)

class SearchPurchaseViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.purch = Purchase.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, cost_price=5000.0, current_stock_level=20,
                                total_stock_level=40,
                                supplier_tel='256710000000',
                                created_by=User.objects.get(username="test"))

        self.username = 'test'
        self.password = '1234@test'

    def test_search_purchase_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('search_purchase'), data={'q': self.purch.name})
        self.assertEqual(resp.status_code, 200)

class SearchProductViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, unit_price=5000.0, stock_level=20, created_by=User.objects.get(username="test"))

        self.username = 'test'
        self.password = '1234@test'
    def test_search_product_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('search_stock'), data={'q': self.prod.name})
        self.assertEqual(resp.status_code, 200)

class SearchExpenseViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.cat = ExpenseCategory.objects.create(name='Transport',
                        description = "This is an expense on cost of transportation",
                        created_by=User.objects.get(username="test"))
        self.exp = Expenses.objects.create(category=self.cat,
                                description="This is the cost of transporting items from kampala.",
                                amount=10000.0,
                                created_by=self.test)
        self.username = 'test'
        self.password = '1234@test'

    def test_search_expense_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('search_expense'), data={'q': self.exp.description})
        self.assertEqual(resp.status_code, 200)
