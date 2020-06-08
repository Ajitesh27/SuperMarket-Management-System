from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, UpdateView, DetailView, DeleteView, CreateView )
from .forms import PurchaseCreationForm, EditPurchaseForm
from .models import Purchase
from decorators.decorators import group_required
from easy_pdf.views import PDFTemplateView
from helpers.generate_pdf import generate_report

decorators = [group_required(['Admin','Manager','General Manager'])]
@method_decorator(decorators, name="dispatch")
class PurchaseListView(ListView):
    queryset = Purchase.objects.all().order_by('id')
    paginate_by = 10
    context_object_name = 'purchase_list'
    template_name = 'purchase/purchase.html'

@method_decorator(decorators, name='dispatch')
class PurchaseCreationView(CreateView):
    form_class = PurchaseCreationForm
    template_name = 'purchase/add_purchase.html'
    success_message = 'Success: Purchase creation succeeded.'
    success_url = reverse_lazy('setting')

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.POST.get('name', None),
            'description': request.POST.get('description', None),
            'quantity': request.POST.get('quantity', 0),
            'cost_price': request.POST.get('cost_price', 0),
            'current_stock_level': request.POST.get('current_stock_level', 0),
            'total_stock_level': int(request.POST.get('quantity', 0)) + int(request.POST.get('current_stock_level', 0)),
            'supplier_tel': request.POST.get('supplier_tel', None),
            'created_by': request.user.id
        }
        if request.method == 'POST':
            form = self.form_class(data)

            if form.is_valid():
                form.save()

                return HttpResponseRedirect(self.success_url)

        return super().post(request, *args, **kwargs)


@method_decorator(decorators, name='dispatch')
class EditPurchaseView(UpdateView, DetailView):
    template_name = 'purchase/edit_purchase.html'
    pk_url_kwarg = 'id'
    form_class = EditPurchaseForm
    queryset = Purchase.objects.all()
    success_url = reverse_lazy('setting')


@method_decorator(decorators, name='dispatch')
class DeletePurchaseView(DeleteView):
    template_name = 'purchase/delete_purchase.html'
    pk_url_kwarg = 'id'
    queryset = Purchase.objects.all()
    success_url = reverse_lazy('setting')

class PurchasePDFView(PDFTemplateView):
    template_name = 'purchase/purchase_report.html'

    def get_context_data(self, **kwargs):
        dataset = Purchase.objects.values(
                                'name','description',
                                'quantity','cost_price',
                                'current_stock_level',
                                'total_stock_level',
                                'supplier_tel').order_by('id')
        context = super(PurchasePDFView, self).get_context_data(
            pagesize='A4',
            title='Purchase Report',
            **kwargs
        )

        return generate_report(context, dataset, 'Purchases List')
