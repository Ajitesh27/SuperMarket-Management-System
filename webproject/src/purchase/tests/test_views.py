from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.models import User, Role
from ..models import Purchase

class PurchaseCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of kakira sugar',
            'quantity': 10,
            'cost_price': 3000.0,
            'current_stock_level': 10,
            'total_stock_level': 20,
            'supplier_tel': '256710000000',
            'created_by': self.test.id
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_purchase_list_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('purchases'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'purchase/purchase.html')

    def test_purchase_creation(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('purchase'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_purchase_count(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse_lazy('purchase'), data=self.data)
        count = Purchase.objects.count()
        self.assertEqual(count, 1)

    def test_purchase_creation_with_no_login(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        response = self.client.post(reverse_lazy('purchase'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_purchase_creation_by_get(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('purchase'))
        self.assertEqual(response.status_code, 200)

class PurchaseEditViewTest(TestCase):
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
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of sugar',
            'quantity': 20,
            'cost_price': 4000.0,
            'current_stock_level': 20,
            'total_stock_level': 40,
            'supplier_tel': '256710000001'
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_edit_purchase_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('edit_purchase', kwargs={'id':self.purch.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'purchase/edit_purchase.html')

    def test_edit_purchase(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_purchase', kwargs={'id':self.purch.id}), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_edit_purchase_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_purchase', kwargs={'id':self.purch.id}))
        self.assertEqual(response.status_code, 200)

class PurchaseDeleteViewTest(TestCase):
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
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of sugar',
            'quantity': 20,
            'cost_price': 4000.0,
            'current_stock_level': 20,
            'total_stock_level': 40,
            'supplier_tel': '256710000001'
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_delete_purchase_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('delete_purchase', kwargs={'id':self.purch.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'purchase/delete_purchase.html')

    def test_delete_purchase(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('delete_purchase', kwargs={'id':self.purch.id}))
        self.assertEqual(response.status_code, 302)

class PurchasePDFViewTest(TestCase):
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
        self.data = {
            'name': 'sugar',
            'description': 'This is a stock of sugar',
            'quantity': 20,
            'cost_price': 4000.0,
            'current_stock_level': 20,
            'total_stock_level': 40,
            'supplier_tel': '256710000001'
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_purchase_pdf_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('purchase_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'purchase/purchase_report.html')
