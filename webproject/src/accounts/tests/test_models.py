from django.test import TestCase
from ..models import User, Role

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("test", "test@info.com", "1234@test")
        User.objects.create_superuser("managertest", "managertest@info.com", "1234@manager")

    def test_regular_user_was_created(self):
        test = User.objects.get(username="test")
       
        self.assertEqual(test.username, "test")
        self.assertEqual(test.email, "test@info.com")

    def test_admin_user_was_created(self):
        admin = User.objects.get(username="managertest")

        self.assertEqual(admin.username, "managertest")
        self.assertEqual(admin.email, "managertest@info.com")

    def test_admin_with_no_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser("", "managertest@info.com", "1234@manager")

    def test_admin_with_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser("managertest", "", "1234@manager")

    def test_admin_with_no_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser("managertest", "managertest@info.com", "")

    def test_regular_user_details_not_equal(self):
        test = User.objects.get(username="test")
       
        self.assertNotEqual(test.username, "tests")
        self.assertNotEqual(test.email, "tests@info.com")

    def test_admin_user_details_not_equal(self):
        admin = User.objects.get(username="test")

        self.assertNotEqual(admin.username, "managertest")
        self.assertNotEqual(admin.email, "managertest@info.com")

    def test_username_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')
    
    def test_username_max_length(self):
        test = User.objects.get(id=3)
        max_length = test._meta.get_field('username').max_length
        self.assertEquals(max_length, 255)

    def test_email_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email address')

    def test_email_max_length(self):
        test = User.objects.get(id=3)
        max_length = test._meta.get_field('email').max_length
        self.assertEquals(max_length, 255)

    def test_password_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('password').verbose_name
        self.assertEquals(field_label, 'password')

    def test_is_admin_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('is_admin').verbose_name
        self.assertEquals(field_label, 'is admin')

    def test_is_active_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('is_active').verbose_name
        self.assertEquals(field_label, 'is active')
    
    def test_created_at_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'created at')
    
    def test_updated_at_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('updated_at').verbose_name
        self.assertEquals(field_label, 'updated at')

    def test_last_login_label(self):
        test = User.objects.get(id=3)
        field_label = test._meta.get_field('last_login').verbose_name
        self.assertEquals(field_label, 'last login')

    def test_user_count(self):
        count = User.objects.count()
        self.assertEqual(count, 3)

    def test_user_get_full_name(self):
        test = User.objects.get(id=4)
        name = test.get_full_name()
        self.assertEqual(name, 'managertest')
    
    def test_user_get_short_name(self):
        test = User.objects.get(id=4)
        name = test.get_short_name()
        self.assertEqual(name, 'managertest')

    def test_user_has_perm(self):
        test = User.objects.get(id=3)
        self.assertTrue(test.has_perm('add_user'))

    def test_user_has_module_perm(self):
        test = User.objects.get(id=3)
        self.assertTrue(test.has_module_perms('accounts'))

    def test_user_is_staff(self):
        test = User.objects.get(id=4)
        self.assertTrue(test.is_staff)

    def test_user_can_be_deleted(self):
        test = User.objects.get(id=3)
        test.delete()
        self.assertFalse(test.is_active)

class RoleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Role.objects.create(name="test", description="This is a test role")
        Role.objects.create(name="manager", description="This is a manager role")

    def test_role_was_created(self):
        test = Role.objects.get(name="test")
        admin = Role.objects.get(name="manager")
       
        self.assertEqual(test.name, "test")
        self.assertEqual(test.description, "This is a test role")

        self.assertEqual(admin.name, "manager")
        self.assertEqual(admin.description, "This is a manager role")

    def test_role_object_return_correct_str_rep(self):
        role = Role.objects.create(name="cleaner", description="This is a cleaner role")
        self.assertEqual(str(role), 'cleaner')

    def test_role_name_label(self):
        test = Role.objects.get(id=2)
        field_label = test._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
    
    def test_role_description_label(self):
        test = Role.objects.get(id=2)
        field_label = test._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')
    
    def test_role_description_max_length(self):
        test = Role.objects.get(id=2)
        max_length = test._meta.get_field('description').max_length
        self.assertEquals(max_length, 100)

    def test_role_count(self):
        count = Role.objects.count()
        self.assertEqual(count, 3)
