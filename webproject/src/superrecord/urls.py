from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from helpers import graphs as graph_view
from . import views as main_view
from django.urls import path, re_path
from stocks import views 
from django.conf.urls import url

urlpatterns = [
    #path('', include('stocks.urls')),
    #re_path('edit_product/([0-9]+)$', product_view.products_detail, name='edit_product'),
    #re_path('delete_product/([0-9]+)$', product_view.products_detail, name='delete_product'),
    #re_path('product_report/$', product_view.ProductPDFView.as_view(), name='product_report'),
    path('admin/', admin.site.urls),
    re_path(r'^api/stocks/$', views.stocks_list),
    re_path(r'^api/stocks/(?P<pk>[0-9]+)$', views.stocks_detail),
    path('', main_view.IndexView.as_view(), name='index'),
    path('reports/', main_view.AccountReportView.as_view(), name='reports'),
    path('reports/accounts/', main_view.AccountListView.as_view(), name='accounts'),
    path('reports/roles/', main_view.RolesListView.as_view(), name='roles'),
    path('reports/stocks/', main_view.StocksListView.as_view(), name='stock_list'),
    path('reports/purchases/', main_view.PurchaseListView.as_view(), name='purchases_list'),
    path('reports/sales/', main_view.SalesListView.as_view(), name='sales_list'),
    path('reports/categories/', main_view.CategoryListView.as_view(), name='categories'),
    path('reports/expenses/', main_view.ExpensesListView.as_view(), name='expenses_list'),
    path('reports/analysis/', main_view.AnalysisView.as_view(), name='analysis'),
    path('company/', include('company.urls')),
    path('accounts/', include('accounts.urls')),
    path('stocks/', include('stocks.urls')),
    path('purchases/', include('purchase.urls')),
    path('sales/', include('sales.urls')),
    path('expenses/', include('expenses.urls')),
    path('transactions/', main_view.TransactionsView.as_view(), name='transactions'),
    path('graphs/roles/', graph_view.roles_graph, name='roles_data'),
    path('graphs/stocks/', graph_view.stocks_graph, name='stocks_data'),
    path('graphs/sales/', graph_view.sales_graph, name='sales_data'),
    path('graphs/expenses/', graph_view.expenses_graph, name='expenses_data'),
    path('search/user/', main_view.SearchUserView.as_view(), name='search_user'),
    path('search/expense/', main_view.SearchExpensesView.as_view(), name='search_expense'),
    path('search/sale/', main_view.SearchSalesView.as_view(), name='search_sale'),
    path('search/purchase/', main_view.SearchPurchaseView.as_view(), name='search_purchase'),
    path('search/stock/', main_view.SearchStockView.as_view(), name='search_stock')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
