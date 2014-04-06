import hashlib
import json

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    Category,
    Company,
    CurrentUrl,
    Media,
)
from .utils import (
    PRODUCT_CLASSES,
    JsonResponse,
    parse_float_price,
)


class HomeView(TemplateView):
    template_name = 'home.html'


@require_POST
@csrf_exempt
def add_current_urls(request):
    data = json.loads(request.POST['data'])
    country_code = request.POST['country_code']
    category_name = request.POST.get('category', '')

    company = Company.objects.get(name__iexact=request.POST['company'])
    category = Category.objects.filter(name__iexact=category_name).first()

    idx = 0
    product_urls = data['product_urls'][idx: idx+10]

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
        product_urls = data['product_urls'][idx: idx+10]
    context = {
        'sucess': True,
    }
    
    return HttpResponse(
        json.dumps(context),
        content_type='application/json'
    )


def get_current_urls(request):
    country_code = request.GET.get('country_code')
    company_name = request.GET.get('company')
    limit = request.GET.get('limit')

    product_urls = list(CurrentUrl.objects.filter(
        country__iexact=country_code,
        company__name__iexact=company_name,
    ).order_by('-added').values('category__name', 'link', 'merchant'))

    if limit:
        product_urls = product_urls[:int(limit)]

    return JsonResponse(content=product_urls)


@require_POST
@csrf_exempt
def save_products(request):
    data = json.loads(request.POST['data'])
    country_code = request.POST['country_code']
    category_name = request.POST.get('category', '')

    product_class = PRODUCT_CLASSES[country_code]

    company = Company.objects.get(name__iexact=request.POST['company'])
    category = Category.objects.filter(name__iexact=category_name).first()

    idx = 0
    products = data['products'][idx: idx+10]

    while products:
        for prod in products:
            url = prod.get('url')
            product, created = product_class.objects.get_or_create(
                link = url,
                company = company,
            )
            if created:
                product_id = prod.get('product_id')
                if not product_id:
                    if url[len(url)-1] == '/':
                        url = url[:len(url)-1]
                    product_id = url.split('/')[-1]
                    product_id = hashlib.sha224(product_id).hexdigest()
                title = prod.get('title')
                description = prod.get('description')
                product.product_id = product_id
                product.title = u'{}'.format(title).encode('utf-8')

                if prod.get('category'):
                    category = Category.objects.filter(name__iexact=prod.get('category')).first()
                product.category = category

                product.company = company
                product.description = u'{}'.format(description).encode('utf-8')
                product.offer_price = parse_float_price(prod.get('offer_price'), country_code)
                product.regular_price = parse_float_price(prod.get('regular_price'), country_code)
                product.merchant = prod.get('merchant')

                if prod.get('media_link'):
                    media = Media.objects.create(
                        link=prod.get('media_link'),
                        caption=prod.get('media_caption')
                    )
                    product.media = media
                product.save()
            CurrentUrl.objects.filter(link=url).delete()
        idx += 10
        products = data['products'][idx: idx+10]

    context = {
        'success': True,
    }
    
    return HttpResponse(
        json.dumps(context),
        content_type='application/json'
    )

