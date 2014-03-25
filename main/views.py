import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from .models import (
    COUNTRY_CHOICES,
    CurrentUrl,
    Company,
)
from .utils import PRODUCT_CLASSES


class HomeView(TemplateView):
    template_name = 'home.html'


@csrf_exempt
def add_current_urls(request):
    data = json.loads(request.POST['data'])
    country_code = request.POST['country_code']

    company = Company.objects.get(name=request.POST['company'])

    for url in data['urls']:
        current_url, created = CurrentUrl.objects.get_or_create(
            company = company,
            country = country_code,
            link = url
            )
    context = {}
    return render(request, 'home.html', context)


class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'products.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        company_id = self.request.GET.get('company_id', 1)
        country_code = self.request.GET.get('country_code', 'sg')
        product_class = PRODUCT_CLASSES[country_code]
        products = product_class.objects.filter(company__id=company_id)
        
        return products