from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, UpdateView, DetailView, DeleteView, CreateView, TemplateView )
from .forms import ( UserRegisterForm, EditProfileForm,
    RoleCreationForm, EditRoleForm )
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import Group
from company.models import Company
from .models import User, Role
from stocks.models import Product
from sales.models import Sales
from purchase.models import Purchase
from expenses.models import ExpenseCategory, Expenses
from .permissions import assign_permissions, remove_permissions
from decorators.decorators import group_required
from easy_pdf.views import PDFTemplateView
from helpers.generate_pdf import generate_report

decorators = [group_required(['Admin','Manager','General Manager'])]
@method_decorator(decorators, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'user_list'
    template_name = 'accounts/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.all().values()[0]

        return context

@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView, DetailView):
    template_name = 'accounts/edit.html'
    pk_url_kwarg = 'id'
    form_class = EditProfileForm
    queryset = User.objects.all()
    success_url = reverse_lazy('setting')
    old_role = []

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(id=kwargs['id'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Group.objects.all().values_list('name', flat=True)

        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['id'])
        self.old_role += user.groups.all().values_list('name', flat=True)
        new_role = request.POST.get('role', None)

        if len(self.old_role) > 0:
            user.groups.remove(Group.objects.get(name=self.old_role[0]))

        if new_role is not None:
            user.groups.add(Group.objects.get(name=new_role))

        return super().post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PasswordUpdateView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    pk_url_kwarg = 'id'
    form_class = PasswordChangeForm
    queryset = User.objects.all()
    success_url = reverse_lazy('setting')

@method_decorator(decorators, name='dispatch')
class DeactivateView(DeleteView):
    template_name = 'accounts/deactivate.html'
    pk_url_kwarg = 'id'
    queryset = User.objects.all()
    success_url = reverse_lazy('setting')

@method_decorator(login_required, name='dispatch')
class ActivateView(DeleteView):
    template_name = 'accounts/activate.html'
    pk_url_kwarg = 'id'
    queryset = User.objects.all()
    success_url = reverse_lazy('setting')

@method_decorator(decorators, name='dispatch')
class SignUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/signup.html'
    success_message = 'Success: Sign up succeeded.'
    success_url = reverse_lazy('setting')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Group.objects.all().values_list('name', flat=True)

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            role_name = request.POST['role']
            user.groups.add(Group.objects.get(name=role_name))

            return HttpResponseRedirect(self.success_url)

        return super().post(request, *args, **kwargs)

@method_decorator(decorators, name='dispatch')
class RoleCreationView(CreateView):
    form_class = RoleCreationForm
    template_name = 'accounts/add_role.html'
    success_message = 'Success: Role creation succeeded.'
    success_url = reverse_lazy('setting')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            role = form.save()

            perm = [request.POST['user_perm']]
            if 'full' in perm:
                assign_permissions(role, perm, full=True)
            else:
                assign_permissions(role, perm)

            return HttpResponseRedirect(self.success_url)

        return super().post(request, *args, **kwargs)

@method_decorator(decorators, name='dispatch')
class RoleListView(ListView):
    queryset = Role.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'role_list'
    template_name = 'accounts/roles.html'

@method_decorator(decorators, name='dispatch')
class EditRoleView(UpdateView, DetailView):
    template_name = 'accounts/edit_role.html'
    pk_url_kwarg = 'id'
    form_class = EditRoleForm
    queryset = Role.objects.all()
    success_url = reverse_lazy('setting')
    old_perms = []

    def get(self, request, *args, **kwargs):
        self.edit_role = Role.objects.get(id=kwargs['id'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_perms'] = self.edit_role.permissions.all().values_list('codename', flat=True)

        return context

    def post(self, request, *args, **kwargs):

        edit_role = Role.objects.get(id=kwargs['id'])
        self.old_perms += edit_role.permissions.all().values_list('codename', flat=True)
        new_perm = request.POST.getlist('user_perm')

        if not new_perm:
            raise ValueError("You must assign atleast 1 permission for the new role")

        if 'full' in new_perm or len(new_perm) == 4:
            edit_role.permissions.remove()
            assign_permissions(edit_role, new_perm, full=True)
        else:
            if len(new_perm) > 1:
                for perm in new_perm:
                    if perm not in self.old_perms:
                        assign_permissions(edit_role, [perm])
                remove_permissions(edit_role, new_perm, self.old_perms)
            else:
                if new_perm not in self.old_perms:
                    assign_permissions(edit_role, new_perm)
                remove_permissions(edit_role, new_perm, self.old_perms)

        return super().post(request, *args, **kwargs)

@method_decorator(decorators, name='dispatch')
class DeleteRoleView(DeleteView):
    template_name = 'accounts/delete_role.html'
    pk_url_kwarg = 'id'
    queryset = Role.objects.all()
    success_url = reverse_lazy('setting')

@method_decorator(login_required, name='dispatch')
class Home(ListView):
    queryset = User.objects.all().order_by('id')
    paginate_by = 10
    template_name = 'accounts/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = len(User.objects.all())
        context['roles'] = len(Group.objects.all())
        context['stocks'] = len(Product.objects.all())
        context['sales'] = len(Sales.objects.all())
        context['purchases'] = len(Purchase.objects.all())
        context['category'] = len(ExpenseCategory.objects.all())
        context['expenses'] = len(Expenses.objects.all())
        context['company'] = Company.objects.all().values()[0]

        return context

@method_decorator(decorators, name='dispatch')
class Setting(TemplateView):
    template_name = 'accounts/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.all()

        return context

class AccountPDFView(PDFTemplateView):
    template_name = 'accounts/account_report.html'

    def get_context_data(self, **kwargs):
        dataset = User.objects.values(
                                'username','groups','email',
                                'is_admin','is_active').order_by('id')
        context = super(AccountPDFView, self).get_context_data(
            pagesize='A4',
            title='Account Report',
            **kwargs
        )
        for data in dataset:
            data['groups'] = Role.objects.get(id=data['groups'])

        return generate_report(context, dataset, 'Accounts List')
