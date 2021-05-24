from django.test import TestCase
from expenses.models import ExpenseCategory, Expenses
from accounts.models import User

class ExpenseCategoryModelTest(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        ExpenseCategory.objects.create(name="purchases",
                                description="This is an expense on cost of purchasing new stocks",
                                created_by=User.objects.get(username="admintest"))

    def test_expense_category_was_created(self):
        category = ExpenseCategory.objects.get(name="purchases")
        self.assertEqual(category.name, "purchases")
        self.assertEqual(category.description, "This is an expense on cost of purchasing new stocks")

    def test_expense_category_object_return_correct_str_rep(self):
        category = ExpenseCategory.objects.create(name="administrative",
                                description="This is an administrative cost",
                                created_by=User.objects.get(username="admintest"))
        self.assertEqual(str(category), 'administrative')

    def test_expense_category_name_label(self):
        category = ExpenseCategory.objects.get(name="purchases")
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_expense_category_description_label(self):
        category = ExpenseCategory.objects.get(name="purchases")
        field_label = category._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_expense_category_name_max_length(self):
        category = ExpenseCategory.objects.get(name="purchases")
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_expense_category_description_max_length(self):
        category = ExpenseCategory.objects.get(name="purchases")
        max_length = category._meta.get_field('description').max_length
        self.assertEquals(max_length, 100)

    def test_expense_category_count(self):
        count = ExpenseCategory.objects.count()
        self.assertEqual(count, 1)

class ExpenseModelTest(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        ExpenseCategory.objects.create(name="purchases",
                                description="This is an expense on cost of purchasing new stocks",
                                created_by=User.objects.get(username="admintest"))
        Expenses.objects.create(category=ExpenseCategory.objects.get(name='purchases'),
                                description="This is the cost of buying 10 bags of sugar",
                                amount=700000,
                                created_by=User.objects.get(username="admintest"))

    def test_expense_was_created(self):
        expense = Expenses.objects.get(description="This is the cost of buying 10 bags of sugar")
        self.assertEqual(expense.description, "This is the cost of buying 10 bags of sugar")

    def test_expense_object_return_correct_str_rep(self):
        expense = Expenses.objects.create(category=ExpenseCategory.objects.get(name='purchases'),
                                description="This is the cost of buying 5 boxes of bar shoap",
                                amount=250000,
                                created_by=User.objects.get(username="admintest"))
        self.assertEqual(str(expense), 'This is the cost of buying 5 boxes of bar shoap')

    def test_expense_name_label(self):
        expense = Expenses.objects.get(description="This is the cost of buying 10 bags of sugar")
        field_label = expense._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_expense_category_description_label(self):
        expense = Expenses.objects.get(description="This is the cost of buying 10 bags of sugar")
        field_label = expense._meta.get_field('amount').verbose_name
        self.assertEquals(field_label, 'amount')

    def test_expense_category_description_max_length(self):
        expense = Expenses.objects.get(description="This is the cost of buying 10 bags of sugar")
        max_length = expense._meta.get_field('description').max_length
        self.assertEquals(max_length, 100)

    def test_expense_amount_is_correct(self):
        expense = Expenses.objects.get(description="This is the cost of buying 10 bags of sugar")
        self.assertEquals(expense.amount, 700000.0)

    def test_expense_category_count(self):
        count = Expenses.objects.count()
        self.assertEqual(count, 1)
