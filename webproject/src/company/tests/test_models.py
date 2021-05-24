from django.test import TestCase
from company.models import Company
from accounts.models import User

class CompanyModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Company.objects.create(
        name="Test Supermarket System",
        address="P.O.Box xxx, Arua",
        company_tel="+25672xxxxxxx",
        created_by= User.objects.get(username="admin")
        )

    def test_expense_object_return_correct_str_rep(self):
        company = Company.objects.get(id=1)
        self.assertEqual(str(company), "Superrecord Management System")

    def test_company_name_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_company_address_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_company_name_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_company_address_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('address').max_length
        self.assertEquals(max_length, 100)

    def test_company_tel_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('company_tel').max_length
        self.assertEquals(max_length, 13)

    def test_expense_category_count(self):
        count = Company.objects.count()
        self.assertEqual(count, 2)
