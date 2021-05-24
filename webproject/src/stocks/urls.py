from django.urls import path,re_path
from stocks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
  #  path('api/', views.products_list),
 #   path('api', views.products_list),
  #  path('api/<int:pk>/', views.products_detail),
    #path('<int:pk>/', views.products_detail.as_view()),
    path('product_report/', views.ProductPDFView.as_view(), name='product_report'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
