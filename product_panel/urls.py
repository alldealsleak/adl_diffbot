from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import ProductListingView, ProductListView

urlpatterns = patterns('',
    url(r'^product-listings', login_required(ProductListingView.as_view()), name='product-listings'),
    url(r'^products', login_required(ProductListView.as_view()), name='products'),
)