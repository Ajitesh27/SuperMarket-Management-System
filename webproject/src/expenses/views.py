from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, UpdateView, DetailView, DeleteView, CreateView)
from decorators.decorators import group_required
from expenses.models import ExpenseCategory, Expenses
from accounts.models import User
from expenses.forms import (
    EditCategoryForm, EditExpenseForm,
    CategoryCreationForm, ExpenseCreationForm)
from easy_pdf.views import PDFTemplateView
from helpers.generate_pdf import generate_report

decorators = [group_required(['Admin','Manager','General Manager'])]
@method_decorator(login_required, name="dispatch")
class CategoryListView(ListView):
    queryset = ExpenseCategory.objects.all().order_by('-id')
    paginate_by = 10
    context_object_name = 'categories'
    template_name = 'expenses/expenses_category.html'

@method_decorator(decorators, name='dispatch')
class CategoryCreationView(CreateView):
    form_class = CategoryCreationForm
    template_name = 'expenses/add_category.html'
    success_message = 'Success: Category creation succeeded.'
    success_url = reverse_lazy('setting')

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.POST.get('name', None),
            'description': request.POST.get('description', None),
            'created_by': request.user.id
        }
        if request.method == 'POST':
            form = self.form_class(data)

            if form.is_valid():
                form.save()

                return HttpResponseRedirect(self.success_url)

        return super().post(request, *args, **kwargs)

@method_decorator(decorators, name='dispatch')
class EditCategoryView(UpdateView, DetailView):
    template_name = 'expenses/edit_category.html'
    pk_url_kwarg = 'id'
    form_class = EditCategoryForm
    queryset = ExpenseCategory.objects.all()
    success_url = reverse_lazy('setting')

@method_decorator(decorators, name='dispatch')
class DeleteCategoryView(DeleteView):
    template_name = 'expenses/delete_category.html'
    pk_url_kwarg = 'id'
    queryset = ExpenseCategory.objects.all()
    success_url = reverse_lazy('setting')

@method_decorator(login_required, name="dispatch")
class ExpensesListView(ListView):
    queryset = Expenses.objects.all().order_by('-id')
    paginate_by = 10
    context_object_name = 'expenses'
    template_name = 'expenses/expenses.html'

@method_decorator(login_required, name='dispatch')
class ExpenseCreationView(CreateView):
    form_class = ExpenseCreationForm
    template_name = 'expenses/add_expense.html'
    success_message = 'Success: Expense creation succeeded.'
    success_url = reverse_lazy('transactions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = Expenses.objects.filter(created_by=self.request.user.id)
        context['total_expenses'] = Expenses.objects.filter(created_by=self.request.user.id).aggregate(Sum('amount'))

        return context

    def post(self, request, *args, **kwargs):
        data = {
            'category': int(request.POST.get('category', 0)),
            'description': request.POST.get('description', None),
            'amount': request.POST.get('amount', 0),
            'created_by': request.user.id
        }
        if request.method == 'POST':
            form = self.form_class(data)

            if form.is_valid():
                form.save()

                return HttpResponseRedirect(self.success_url)

        return super().post(request, *args, **kwargs)

@method_decorator(decorators, name='dispatch')
class EditExpenseView(UpdateView, DetailView):
    template_name = 'expenses/edit_expense.html'
    pk_url_kwarg = 'id'
    form_class = EditExpenseForm
    queryset = Expenses.objects.all()
    success_url = reverse_lazy('transactions')

@method_decorator(decorators, name='dispatch')
class DeleteExpenseView(DeleteView):
    template_name = 'expenses/delete_expense.html'
    pk_url_kwarg = 'id'
    queryset = Expenses.objects.all()
    success_url = reverse_lazy('transactions')

class ExpensesPDFView(PDFTemplateView):
    template_name = 'expenses/expenses_report.html'

    def get_context_data(self, **kwargs):
        dataset = Expenses.objects.values(
                                'category','description',
                                'amount',
                                'created_by',
                                'created_at').order_by('id')
        context = super(ExpensesPDFView, self).get_context_data(
            pagesize='A4',
            title='Expenses Report',
            **kwargs
        )
        for data in dataset:
            data['created_by'] = User.objects.get(id=data['created_by'])
            data['category'] = ExpenseCategory.objects.get(id=data['category'])

        return generate_report(context, dataset, 'Expenses List')
