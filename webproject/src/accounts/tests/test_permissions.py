from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from ..models import User, Role
from ..permissions import assign_permissions, remove_permissions

class PermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("test", "test@info.com", "1234@test")
        User.objects.create_superuser("admintest", "admintest@info.com", "1234@admin")
        Role.objects.create(name="test", description="This is a test role")
        Role.objects.create(name="admin", description="This is a admin role")

    def test_assign_permission_with_null(self):
        with self.assertRaises(ValueError):
            assign_permissions(None,None)
    
    def test_assign_permission_with_full_permission(self):
        test = Role.objects.get(name="test")
        perm = ["add_user","change_user","delete_user","view_user"]
        test_roles = []
        assign_permissions(test,perm,full=True)

        test_roles += test.permissions.all().values_list('codename', flat=True)
        self.assertEqual(test_roles, perm)

    def test_assign_permission_with_2_permission(self):
        test = Role.objects.get(name="test")
        perm = ["change_user","view_user"]
        test_roles = []
        assign_permissions(test,perm)

        test_roles += test.permissions.all().values_list('codename', flat=True)
        self.assertEqual(test_roles, perm)

    def test_remove_permission(self):
        test = Role.objects.get(name="test")
        perm = ["add_user","change_user","delete_user","view_user"]
        new_perm = ["change_user","view_user"]
        all_perms = []
        test_roles = []
        # test permissions after addition
        assign_permissions(test,perm,full=True)
        all_perms += test.permissions.all().values_list('codename', flat=True)
        self.assertEqual(all_perms, perm)

        # test permissions after removal
        remove_permissions(test,new_perm,perm)
        test_roles += test.permissions.all().values_list('codename', flat=True)
        self.assertEqual(test_roles, new_perm)
