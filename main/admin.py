from django.contrib import admin

from .models import (
    Category,
    Company,
    CurrentUrl,
    ProductSingapore,
    ProductVietnam,
)


class CurrentUrlAdmin(admin.ModelAdmin):
    list_display = ('country', 'company', 'category', 'link', 'added')
    list_filter = ('country', 'company', 'category', 'added')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'title', 'category', 'offer_price', 'company', 'link_method', 'image_tag')
    list_filter = ('company', 'category', 'updated', 'created')

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
admin.site.register(Category)
admin.site.register(CurrentUrl, CurrentUrlAdmin)
admin.site.register(ProductSingapore, ProductAdmin)
admin.site.register(ProductVietnam, ProductAdmin)