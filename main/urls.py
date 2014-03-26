from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import ProductListingView, ProductListView

urlpatterns = patterns('',
    url(r'^products', ProductListView.as_view(), name='products'),
)