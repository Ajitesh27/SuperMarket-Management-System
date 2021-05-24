from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.models import User, Role
from stocks.models import Product
from sales.models import Sales

class SalesCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.test.save()
        self.role.save()
        self.data = {
            'name': self.prod.name,
            'item': self.prod.name,
            'quantity': 10,
            'unit_price': self.prod.unit_price,
            'total_amount': self.prod.unit_price * 10,
            'sold_by': self.test.id
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_sales_list_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('sales'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales/sales.html')

    def test_sales_creation(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('sale'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_sales_count(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse_lazy('sale'), data=self.data)
        count = Sales.objects.count()
        self.assertEqual(count, 1)

    def test_sales_creation_with_no_login(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        response = self.client.post(reverse_lazy('sale'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_sales_creation_by_get(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('sale'))
        self.assertEqual(response.status_code, 200)

class SalesEditViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.sale = Sales.objects.create(name=self.prod.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.data = {
            'item': self.prod.id,
            'quantity': 8
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_edit_sale_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('edit_sale', kwargs={'id':self.sale.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/edit_sale.html')

    def test_edit_sale(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_sale', kwargs={'id':self.sale.id}), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_edit_sale_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_sale', kwargs={'id':self.sale.id}))
        self.assertEqual(response.status_code, 200)

class SalesDeleteViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.sale = Sales.objects.create(name=self.prod.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.username = 'test'
        self.password = '1234@test'

    def test_delete_sale_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('delete_sale', kwargs={'id':self.sale.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/delete_sale.html')

    def test_delete_sale(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('delete_sale', kwargs={'id':self.sale.id}))
        self.assertEqual(response.status_code, 302)

class SalesCheckoutViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.sale = Sales.objects.create(name=self.prod.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.data = {
            'total_amount': 10000,
            'amount_received': 15000
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_sale_checkout_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/checkout.html')

    def test_sale_checkout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('checkout'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_sale_checkout_reduce_prod(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse_lazy('checkout'), data=self.data)
        prod = Product.objects.get(name='books')
        self.assertEqual(prod.stock_level, 25)

    def test_sale_checkout_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('checkout'))
        self.assertEqual(response.status_code, 200)

class SalesPDFViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.sale = Sales.objects.create(name=self.prod.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.username = 'test'
        self.password = '1234@test'

    def test_sales_pdf_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('sales_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/sales_report.html')

class PrintReceiptViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="books", description="This is a stock of books",
                                quantity=30, unit_price=2000.0, stock_level=30,
                                created_by=User.objects.get(username="test"))
        self.sale = Sales.objects.create(name=self.prod.name,
                            item=self.prod,
                            quantity=5, unit_price=self.prod.unit_price,
                            total_amount=self.prod.unit_price * 5,
                            sold_by=User.objects.get(username="test"))
        self.username = 'test'
        self.password = '1234@test'

    def test_sales_receipt_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('sales_receipt'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/sales_receipt.html')
