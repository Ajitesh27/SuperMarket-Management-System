from django.test import TestCase
from accounts.models import User
from expenses.models import ExpenseCategory
from expenses.forms import (
    CategoryCreationForm, EditCategoryForm,
    ExpenseCreationForm, EditExpenseForm)

class CategoryCreationFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.cat_creater = CategoryCreationForm()
        self.cat_creater2 = CategoryCreationForm(
            data={
                'name': "purchases",
                'description': "This is an expense on cost of purchasing new stocks",
                'created_by': self.test.id
            }
        )

    def test_expense_category_name_field_label(self):
        self.assertFalse(self.cat_creater.fields['name'].label is None)
        self.assertFalse(self.cat_creater.fields['name'].label == 'name')

    def test_expense_category_description_field_label(self):
        self.assertFalse(self.cat_creater.fields['description'].label is None)
        self.assertFalse(self.cat_creater.fields['description'].label == 'description')

    def test_expense_category_form_is_valid(self):
        self.assertTrue(self.cat_creater2.is_valid())

    def test_expense_category_form_is_not_valid(self):
        self.assertFalse(self.cat_creater.is_valid())

class EditCategoryFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.cat_creater = EditCategoryForm()
        self.cat_creater2 = EditCategoryForm(
            data={
                'name': "Transport",
                'description': "This is the cost of transportation",
                'sold_by': self.test.id
            }
        )

    def test_expense_category_name_field_label(self):
        self.assertFalse(self.cat_creater.fields['name'].label is None)
        self.assertFalse(self.cat_creater.fields['name'].label == 'name')

    def test_expense_category_description_field_label(self):
        self.assertFalse(self.cat_creater.fields['description'].label is None)
        self.assertFalse(self.cat_creater.fields['description'].label == 'description')

    def test_expense_category_form_is_valid(self):
        self.assertTrue(self.cat_creater2.is_valid())

    def test_expense_category_form_is_not_valid(self):
        self.assertFalse(self.cat_creater.is_valid())

class ExpenseCreationFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.cat = ExpenseCategory.objects.create(name="purchases",
                                description="This is an expense on cost of purchasing new stocks",
                                created_by=User.objects.get(username="test"))
        self.cat_creater = ExpenseCreationForm()
        self.cat_creater2 = ExpenseCreationForm(
            data={
                'category': self.cat.id,
                'description': "This is the cost of buying a bag sugar",
                'amount': 70000.0,
                'created_by': self.test.id
            }
        )

    def test_expense_amount_field_label(self):
        self.assertFalse(self.cat_creater.fields['amount'].label is None)
        self.assertFalse(self.cat_creater.fields['amount'].label == 'amount')

    def test_expense_description_field_label(self):
        self.assertFalse(self.cat_creater.fields['description'].label is None)
        self.assertFalse(self.cat_creater.fields['description'].label == 'description')

    def test_expense_form_is_valid(self):
        self.assertTrue(self.cat_creater2.is_valid())

    def test_expense_form_is_not_valid(self):
        self.assertFalse(self.cat_creater.is_valid())

class EditExpenseFormTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.cat_creater = EditExpenseForm()
        self.cat_creater2 = EditExpenseForm(
            data={
                'amount': 65000.0,
                'description': "This is the cost of buying a bag sugar"
            }
        )

    def test_expense_amount_field_label(self):
        self.assertFalse(self.cat_creater.fields['amount'].label is None)
        self.assertFalse(self.cat_creater.fields['amount'].label == 'amount')

    def test_expense_description_field_label(self):
        self.assertFalse(self.cat_creater.fields['description'].label is None)
        self.assertFalse(self.cat_creater.fields['description'].label == 'description')

    def test_expense_form_is_valid(self):
        self.assertTrue(self.cat_creater2.is_valid())

    def test_expense_form_is_not_valid(self):
        self.assertFalse(self.cat_creater.is_valid())
