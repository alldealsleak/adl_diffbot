from django.contrib import admin

from .models import ProductSingapore, Company, CurrentUrl


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'title', 'offer_price', 'company', 'link_method', 'image_tag')

    def __init__(self,*args,**kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)

    def link_method(self, obj):
        return u'<a href="{0}">{0}</a>'.format(obj.link)
    link_method.allow_tags = True
    link_method.short_description = 'Link'

    def image_tag(self, obj):
        if obj.media:
            return u'<img src="{}" style="width: 50px; height: 75px;"/>'.format(obj.media.link)
        return None
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

admin.site.register(Company)
admin.site.register(CurrentUrl)
admin.site.register(ProductSingapore, ProductAdmin)