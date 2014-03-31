import json

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Category,
    CurrentUrl,
    Company,
)


class HomeView(TemplateView):
    template_name = 'home.html'


@csrf_exempt
def add_current_urls(request):
    data = json.loads(request.POST['data'])
    country_code = request.POST['country_code']
    category_name = request.POST.get('category', '')

    company = Company.objects.get(name__iexact=request.POST['company'])
    category = Category.objects.filter(name__iexact=category_name).first()

    idx = 0
    product_urls = data['product_urls'][idx: idx+1]

    while product_urls:
        for product in product_urls:
            current_url, created = CurrentUrl.objects.get_or_create(
                company = company,
                country = country_code,
                category = category,
                merchant = product['merchant'].strip(),
                link = product['url']
                )
        idx += 10
        # product_urls = data['product_urls'][idx: idx+10]
    context = {
        'data': data['product_urls'],
    }
    
    return HttpResponse(
        json.dumps(context),
        content_type='application/json',
        **response_kwargs
    )
