from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from ..models import User, Role

class UserListViewTest(TestCase):
    def setUp(self):
        pagenate_num = 10

        for user_id in range(pagenate_num):
            test = User.objects.create_user(
                f"test{user_id}",
                f"test{user_id}@info.com",
                f"1234@test{user_id}"
            )
            test.save()
        self.test1 = User.objects.create_user("man", "test@info.com", "1234@test")
        role = Role.objects.create(name="Manager", description="This is a test role")
        role.save()
        self.test1.save() 

    def test_index_url(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_url(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_works_with_correct_values(self):
        response = self.client.login(username='test1', password='1234@test1')
        self.assertTrue(response)
    
    def test_login_fails_with_in_correct_values(self):
        response = self.client.login(username='man', password='1234@test0')
        self.assertFalse(response)

    def test_home_redirects_without_login(self):
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_home_does_not_redirect_when_login(self):
        self.client.login(username='test1', password='1234@test1')
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(str(response.context['user']), 'test1')
        self.assertEqual(response.status_code, 200)

    def test_settings_can_be_accessed(self):
        self.test1.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='man', password='1234@test')
        response = self.client.get(reverse_lazy('setting'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_be_accessed(self):
        self.test1.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='man', password='1234@test')
        response = self.client.get(reverse_lazy('user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user.html')
        
    def test_user_list_pagination_is_10(self):
        self.test1.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='man', password='1234@test')
        response = self.client.get(reverse_lazy('user'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['user_list']) == 10)

    def test_user_list_second_pagination_is_2(self):
        self.test1.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='man', password='1234@test')
        response = self.client.get(reverse_lazy('user')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['user_list']) == 2)


class UserCreateViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test.save()
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.role.save()

    def test_user_registration_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_user_registration(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        data={'username':'test1','email':'test1@info.com','password1':'1234@test1','password2':'1234@test1','role':'Manager'}
        response = self.client.post(reverse_lazy('signup'), data)
        self.assertEqual(response.status_code, 302)

    def test_user_registration_fails_with_invalid_email(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        data={'username':'test1','email':'test1info.com','password':'1234@test1','role':'Manager'}
        response = self.client.post(reverse_lazy('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


class UserEditViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
        self.role = Role.objects.create(name="test", description="This is a test role")
        self.role2 = Role.objects.create(name="Manager", description="This is an manager role")
        self.test.save()
        self.role.save()
        self.role2.save()
        self.test2.save()

    def test_user_edit_can_be_accessed(self):
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('edit', kwargs={'id':self.test.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit.html')

    def test_user_profile_edit(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        data={'username':'test1','email':'test1@info.com','role':'Admin'}
        response = self.client.post(reverse_lazy('edit', kwargs={'id':self.test.id}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,reverse_lazy('setting'))
    
    def test_edit_user_role(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.test2.groups.add(Group.objects.get(name='test'))
        self.client.login(username='test', password='1234@test')
        data={'username':'test2','email':'test2@info.com','role':'Manager'}
        response = self.client.post(reverse_lazy('edit', kwargs={'id':self.test2.id}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,reverse_lazy('setting'))
        data={'username':'test1','email':'test1@info.com','role':'Manager'}
        response = self.client.post(reverse_lazy('edit', kwargs={'id':self.test.id}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,reverse_lazy('setting'))

    def test_user_login_after_edit(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        data={'username':'test1','email':'test1@info.com'}
        response = self.client.post(reverse_lazy('edit', kwargs={'id':self.test.id}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,reverse_lazy('setting'))
        self.client.logout()
        resp = self.client.login(username='test1', password='1234@test')
        self.assertTrue(resp)
        self.assertRedirects(response,reverse_lazy('setting'))


class UserDeactivateViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
        role = Role.objects.create(name="Manager", description="This is a test role")
        self.test.save()
        role.save()
        self.test2.save()

    def test_user_deactivate_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('deactivate', kwargs={'id':self.test2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/deactivate.html')


class UserActivateViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
        role = Role.objects.create(name="Manager", description="This is a test role")
        self.test.save()
        role.save()
        self.test2.save()

    def test_user_activate_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('activate', kwargs={'id':self.test2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/activate.html')


class RoleCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        self.role.save()

    def test_role_create_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('roles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/roles.html')

    def test_role_creation(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        data={'name':'test','description':'This is a test role', 'user_perm':['change_user','view_user']}
        response = self.client.post(reverse_lazy('role'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_role_creation_with_no_login(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        data={'name':'test','description':'This is a test role', 'user_perm':['change_user','view_user']}
        response = self.client.post(reverse_lazy('role'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_role_creation_by_admin(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        data={'name':'test1','description':'This is a test1 role', 'user_perm':'full'}
        response = self.client.post(reverse_lazy('role'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_role_creation_by_get(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        response = self.client.post(reverse_lazy('role'))
        self.assertEqual(response.status_code, 200)


class RoleEditViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        self.role.save()
        test.groups.add(Group.objects.get(name='Manager'))

    def test_edit_role_can_be_accessed(self):
        self.client.login(username='test', password='1234@test')
        resp = self.client.get(reverse_lazy('edit_role', kwargs={'id':self.role.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/edit_role.html')

    def test_edit_role(self):
        self.client.login(username='test', password='1234@test')
        data={'name':'test2','description':'This is a test2 role', 'user_perm':'view_user'}
        response = self.client.post(reverse_lazy('edit_role', kwargs={'id':self.role.id}), data=data)
        self.assertEqual(response.status_code, 302)

    def test_edit_role_with_full_permission(self):
        self.client.login(username='test', password='1234@test')
        data={'name':'test2','description':'This is a test2 role', 'user_perm':'full'}
        response = self.client.post(reverse_lazy('edit_role', kwargs={'id':self.role.id}), data=data)
        self.assertEqual(response.status_code, 302)

    def test_edit_role_with_2_permission(self):
        self.client.login(username='test', password='1234@test')
        data={'name':'test2','description':'This is a test2 role', 'user_perm':['change_user','view_user']}
        response = self.client.post(reverse_lazy('edit_role', kwargs={'id':self.role.id}), data=data)
        self.assertEqual(response.status_code, 302)
    
    def test_edit_role_by_get(self):
        self.client.login(username='test', password='1234@test')
        with self.assertRaises(ValueError):
            self.client.post(reverse_lazy('edit_role', kwargs={'id':self.role.id}))

class AccountPDFViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
        role = Role.objects.create(name="Manager", description="This is a test role")
        self.test.save()
        role.save()
        self.test2.save()

    def test_account_pdf_can_be_accessed(self):
        self.test.groups.add(Group.objects.get(name='Manager'))
        self.test2.groups.add(Group.objects.get(name='Manager'))
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('account_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/account_report.html')
