from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from company.models import Company
from accounts.models import User, Role
from stocks.models import Product
from purchase.models import Purchase
from sales.models import Sales
from expenses.models import ExpenseCategory, Expenses

class IndexView(TemplateView):
    template_name = 'accounts/index.html'

@method_decorator(login_required, name='dispatch')
class AccountReportView(TemplateView):
    template_name = 'reports/reports.html'

@method_decorator(login_required, name='dispatch')
class AccountListView(ListView):
    queryset = User.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'account_list'
    template_name = 'reports/accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.all().values()[0]

        return context

class SearchUserView(ListView):
    queryset = User.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'account_list'
    template_name = 'reports/accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = User.objects.filter(username__icontains=self.request.GET.get('q', None))

        return context

@method_decorator(login_required, name='dispatch')
class RolesListView(ListView):
    queryset = Role.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'roles'
    template_name = 'reports/roles.html'

@method_decorator(login_required, name='dispatch')
class StocksListView(ListView):
    queryset = Product.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'stocks'
    template_name = 'reports/stocks.html'

class SearchStockView(ListView):
    queryset = Product.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'stocks'
    template_name = 'reports/stocks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocks'] = Product.objects.filter(name__icontains=self.request.GET.get('q', None))

        return context

@method_decorator(login_required, name='dispatch')
class PurchaseListView(ListView):
    queryset = Purchase.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'purchases'
    template_name = 'reports/purchases.html'

class SearchPurchaseView(ListView):
    queryset = Purchase.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'purchases'
    template_name = 'reports/purchases.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.filter(name__icontains=self.request.GET.get('q', None))

        return context

@method_decorator(login_required, name='dispatch')
class SalesListView(ListView):
    queryset = Sales.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'sales_list'
    template_name = 'reports/sales.html'

class SearchSalesView(ListView):
    queryset = Sales.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'sales_list'
    template_name = 'reports/sales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales_list'] = Sales.objects.filter(name__icontains=self.request.GET.get('q', None))

        return context

@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    queryset = ExpenseCategory.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'category_list'
    template_name = 'reports/category.html'

@method_decorator(login_required, name='dispatch')
class ExpensesListView(ListView):
    queryset = Expenses.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'expenses_list'
    template_name = 'reports/expenses.html'

class SearchExpensesView(ListView):
    queryset = Expenses.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'expenses_list'
    template_name = 'reports/expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses_list'] = Expenses.objects.filter(description__icontains=self.request.GET.get('q', None))

        return context

@method_decorator(login_required, name='dispatch')
class AnalysisView(TemplateView):
    template_name = 'reports/analysis.html'

@method_decorator(login_required, name='dispatch')
class TransactionsView(TemplateView):
    template_name = 'transactions/transactions.html'
