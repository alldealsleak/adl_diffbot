from django.contrib import admin

from .models import ProductSingapore, Company, CurrentUrl


admin.site.register(Company)
admin.site.register(CurrentUrl)
admin.site.register(ProductSingapore)