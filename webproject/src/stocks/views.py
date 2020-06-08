from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, UpdateView, DetailView, DeleteView, CreateView )
from easy_pdf.views import PDFTemplateView
from .forms import ProductCreationForm, EditProductForm
from .models import Product
from decorators.decorators import group_required
from helpers.generate_pdf import generate_report




from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from .models import Product
from .serializers import *

@api_view(['GET', 'POST'])
def stocks_list(request):
    if request.method == 'GET':
        data = Product.objects.all()

        serializer = ProductSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def stocks_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data,context={'request': request})
        if serializer.is_valid():
          serializer.save()
          return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductPDFView(PDFTemplateView):
    template_name = 'stocks/product_report.html'

    def get_context_data(self, **kwargs):
        dataset = Product.objects.values(
                                'name','description',
                                'quantity','unit_price',
                                'stock_level').order_by('id')
        context = super(ProductPDFView, self).get_context_data(
            pagesize='A4',
            title='Stock Report',
            **kwargs
        )

        return generate_report(context, dataset, 'Products List')


