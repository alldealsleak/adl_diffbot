from django.db import connection
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from main.models import (
    COUNTRY_CHOICES,
    Company,
)
from main.mixins import JSONResponseMixin
from main.utils import (
    PRODUCT_CLASSES,
    PRODUCT_TABLES,
    CURRENCY_CODES,
)
from .utils import display_product_row


class ProductListingView(TemplateView):
    template_name = 'product-listings.html'

    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()
        context = {
            'countries': COUNTRY_CHOICES,
            'companies': companies,
        }
        return render(request, self.template_name, context)


class ProductListView(JSONResponseMixin, ListView):
    template_name = 'products.html'
    context_object_name = 'product_list'
    output = {}

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        if self.request.is_ajax():
            prod_arr = []
            for product in self.products:
                prod_arr.append(display_product_row(product, self.country_code))

            self.output.update({
                "sEcho" : int(self.request.GET.get('sEcho', 1)),
                "iTotalRecords" : self.total_records,
                "iTotalDisplayRecords" : self.total_records,
                "aaData" : prod_arr
            })

            context.update(self.output)
        return context

    def get_queryset(self):
        p_columns = [
            'title',
            'main_company.name',
            'merchant',
            'main_category.name',
            'created',
            'offer_price',
            'regular_price',
            'main_media.link',
        ]
        company_ids = self.request.GET.getlist('companies', [])
        company_ids = [int(id) for id in company_ids]
        if len(company_ids) > 1:
            company_ids_str = str(company_ids).strip('[]')
        elif len(company_ids) == 1:
            company_ids_str = company_ids[0]
        else:
            company_ids_str = '0'
        self.country_code = self.request.GET.get('country_code', 'sg')

        i_start = self.request.GET.get('iDisplayStart', 0)
        i_length = self.request.GET.get('iDisplayLength', 10)
        i_sort = int(self.request.GET.get('iSortCol_0', 0))
        s_sort_dir = self.request.GET.get('sSortDir_0', 'asc')
        s_search = self.request.GET.get('sSearch', '')

        cur = connection.cursor()

        query_str = """
                SELECT product_id, title, main_company.name, merchant,
                extract(epoch from {0}.created) as created,
                offer_price, regular_price, {0}.link, main_media.link,
                main_category.name
                FROM {0} LEFT JOIN main_media ON 
                {0}.media_id=main_media.id
                JOIN main_category ON
                {0}.category_id=main_category.id
                JOIN main_company ON
                {0}.company_id=main_company.id WHERE
                {0}.company_id IN ({6})
                AND title ILIKE '%{1}%'
                ORDER BY {4} {5}
                LIMIT {2} OFFSET {3}
                """.format(
                    PRODUCT_TABLES[self.country_code],
                    s_search,
                    i_length,
                    i_start,
                    p_columns[i_sort],
                    s_sort_dir,
                    company_ids_str,
                )
        cur.execute(query_str)
        self.products = cur.fetchall()

        self.total_records = PRODUCT_CLASSES[self.country_code].objects.filter(
            title__icontains=s_search, company__in=company_ids
        ).count()
        
        return self.products

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.is_ajax():
            return self.render_to_json_response(self.output)
        else:
            return super(ProductListView, self).render_to_response(context)