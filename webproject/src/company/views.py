from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from .forms import EditCompanyForm
from .models import Company
from decorators.decorators import group_required

decorators = [group_required(['Admin','Manager','General Manager'])]

@method_decorator(decorators, name='dispatch')
class EditCompanyView(UpdateView, DetailView):
    template_name = 'company/company.html'
    pk_url_kwarg = 'id'
    form_class = EditCompanyForm
    queryset = Company.objects.all()
    success_url = reverse_lazy('setting')
