from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^add-current-urls/$', 'main.views.add_current_urls', name='add-current-urls'),
    url(r'^admin/', include(admin.site.urls)),
)
