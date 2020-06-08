from django.urls import path
from purchase import views as purchase_views

urlpatterns = [
    path('purchases/', purchase_views.PurchaseListView.as_view(), name='purchases'),
    path('purchase/', purchase_views.PurchaseCreationView.as_view(), name='purchase'),
    path('edit_purchase/<int:id>/', purchase_views.EditPurchaseView.as_view(), name='edit_purchase'),
    path('delete_purchase/<int:id>/', purchase_views.DeletePurchaseView.as_view(), name='delete_purchase'),
    path('purchase_report/', purchase_views.PurchasePDFView.as_view(), name='purchase_report')
]
