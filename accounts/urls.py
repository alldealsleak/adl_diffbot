from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import LoginView

urlpatterns = patterns('',
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'
    ),
    # url(r'^signup', SignupView.as_view(), name='signup'),
    # url(r'^settings', ProfileUpdateView.as_view(), name='account-settings'),
)