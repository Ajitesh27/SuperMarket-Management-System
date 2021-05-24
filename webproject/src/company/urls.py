from django.urls import path
from company import views as company_views

urlpatterns = [
    path('<int:id>/edit/', company_views.EditCompanyView.as_view(), name='edit_company')
]
