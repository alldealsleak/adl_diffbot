import json

from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import (
    CurrentUrl,
    Company,
)


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
