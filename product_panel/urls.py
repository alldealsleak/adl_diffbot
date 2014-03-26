from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import ProductListingView, ProductListView

urlpatterns = patterns('',
    url(r'^product-listings', ProductListingView.as_view(), name='product-listings'),
    url(r'^products', ProductListView.as_view(), name='products'),
)