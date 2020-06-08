from django.urls import path
from expenses import views as expenses_views

urlpatterns = [
    path('categories/', expenses_views.CategoryListView.as_view(), name='categories'),
    path('category/', expenses_views.CategoryCreationView.as_view(), name='category'),
    path('edit_category/<int:id>/', expenses_views.EditCategoryView.as_view(), name='edit_category'),
    path('delete_category/<int:id>/', expenses_views.DeleteCategoryView.as_view(), name='delete_category'),
    path('expenses/', expenses_views.ExpensesListView.as_view(), name='expenses'),
    path('expense/', expenses_views.ExpenseCreationView.as_view(), name='expense'),
    path('edit_expense/<int:id>/', expenses_views.EditExpenseView.as_view(), name='edit_expense'),
    path('delete_expense/<int:id>/', expenses_views.DeleteExpenseView.as_view(), name='delete_expense'),
    path('expenses_report/', expenses_views.ExpensesPDFView.as_view(), name='expenses_report')
]
