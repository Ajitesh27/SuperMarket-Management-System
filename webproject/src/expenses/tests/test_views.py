from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.models import User, Role
from expenses.models import ExpenseCategory, Expenses

class CategoryCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager",
                                        description="This is a manager role")
        self.test.save()
        self.role.save()
        self.data = {
            'name': "purchases",
            'description': "This is an expense on cost of purchasing new stocks",
            'created_by': self.test.id
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_category_list_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/expenses_category.html')

    def test_category_creation(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('category'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_category_count(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse_lazy('category'), data=self.data)
        count = ExpenseCategory.objects.count()
        self.assertEqual(count, 1)

    def test_category_creation_with_no_login(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        response = self.client.post(reverse_lazy('category'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_category_creation_by_get(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('category'))
        self.assertEqual(response.status_code, 200)

class EditCategoryViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))
        self.cat = ExpenseCategory.objects.create(name='Transport',
                        description = "This is an expense on cost of transportation",
                        created_by=User.objects.get(username="test"))
        self.data = {
            'name': self.cat,
            'description': "This is a category for cost incurred on transporting"
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_edit_category_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('edit_category', kwargs={'id':self.cat.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'expenses/edit_category.html')

    def test_edit_category(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_category', kwargs={'id':self.cat.id}), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_edit_category_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_category', kwargs={'id':self.cat.id}))
        self.assertEqual(response.status_code, 200)

class DeleteCategoryViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.cat = ExpenseCategory.objects.create(name="Transportation",
                            description="This is the cost of transports incurred",
                            created_by=User.objects.get(username="test"))
        self.username = 'test'
        self.password = '1234@test'

    def test_delete_category_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('delete_category', kwargs={'id':self.cat.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'expenses/delete_category.html')

    def test_delete_category(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('delete_category', kwargs={'id':self.cat.id}))
        self.assertEqual(response.status_code, 302)

class ExpenseCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager",
                                        description="This is a manager role")
        self.cat = ExpenseCategory.objects.create(name="purchases",
                                description="This is an expense on cost of purchasing new stocks",
                                created_by=User.objects.get(username="test"))
        self.test.save()
        self.role.save()
        self.cat.save()
        self.data = {
            'category': self.cat.id,
            'description': "This is the cost of buying 10 bags of sugar",
            'amount': 700000.0,
            'created_by': self.test.id
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_expense_list_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/expenses.html')

    def test_expense_creation(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('expense'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_expense_count(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse_lazy('expense'), data=self.data)
        count = Expenses.objects.count()
        self.assertEqual(count, 1)

    def test_expense_creation_with_no_login(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        response = self.client.post(reverse_lazy('expense'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_expense_creation_by_get(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('expense'))
        self.assertEqual(response.status_code, 200)

class EditExpenseViewTest(TestCase):
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
        self.data = {
            'category': self.cat.id,
            'description': "This is the cost of transporting stock items from kampala by bus.",
            'amount': 15000.0,
            'created_by': self.test.id
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_edit_expense_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('edit_expense', kwargs={'id':self.exp.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'expenses/edit_expense.html')

    def test_edit_category(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_expense', kwargs={'id':self.exp.id}), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_edit_category_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('edit_expense', kwargs={'id':self.exp.id}))
        self.assertEqual(response.status_code, 200)

class DeleteExpenseViewTest(TestCase):
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

    def test_delete_expense_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('delete_expense', kwargs={'id':self.exp.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'expenses/delete_expense.html')

    def test_delete_expense(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('delete_expense', kwargs={'id':self.exp.id}))
        self.assertEqual(response.status_code, 302)

class ExpensePDFViewTest(TestCase):
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

    def test_expense_pdf_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse_lazy('expenses_report'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'expenses/expenses_report.html')
