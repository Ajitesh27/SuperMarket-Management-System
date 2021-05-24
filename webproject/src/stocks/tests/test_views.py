from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.models import User, Role
from ..models import Product

class ProductCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.data = {
            'name': 'test',
            'description': 'This is a test product',
            'quantity': 10,
            'unit_price': 1000.0,
            'stock_level': 10,
            'created_by': self.test.id
        }
        self.username = 'test'
        self.password = '1234@test'
    def test_product_list_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/products.html')

    def test_product_creation(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_product_count(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse_lazy('product'), data=self.data)
        count = Product.objects.count()
        self.assertEqual(count, 1)

    def test_product_creation_with_no_login(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        response = self.client.post(reverse_lazy('product'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_product_creation_by_get(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product'))
        self.assertEqual(response.status_code, 200)


class ProductEditViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, unit_price=5000.0, stock_level=20, created_by=User.objects.get(username="test"))
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of sugar',
            'quantity': 20,
            'unit_price': 4000.0,
            'stock_level': 20
        }
        self.username = 'test'
        self.password = '1234@test'
    def test_edit_product_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('edit_product', kwargs={'id':self.prod.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stocks/edit_product.html')

    def test_edit_product(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_product', kwargs={'id':self.prod.id}), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_edit_product_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_product', kwargs={'id':self.prod.id}))
        self.assertEqual(response.status_code, 200)

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, unit_price=5000.0, stock_level=20, created_by=User.objects.get(username="test"))
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of sugar',
            'quantity': 20,
            'unit_price': 4000.0,
            'stock_level': 20
        }
        self.username = 'test'
        self.password = '1234@test'
    def test_delete_product_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('delete_product', kwargs={'id':self.prod.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stocks/delete_product.html')

    def test_delete_product(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('delete_product', kwargs={'id':self.prod.id}))
        self.assertEqual(response.status_code, 302)

class ProductPDFViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.prod = Product.objects.create(name="bread", description="This is a stock of bread",
                                quantity=20, unit_price=5000.0, stock_level=20, created_by=User.objects.get(username="test"))
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of sugar',
            'quantity': 20,
            'unit_price': 4000.0,
            'stock_level': 20
        }
        self.username = 'test'
        self.password = '1234@test'
    def test_product_pdf_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('product_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stocks/product_report.html')
