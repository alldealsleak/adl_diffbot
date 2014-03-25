from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from main.views import HomeView

admin.autodiscover()



urlpatterns = patterns('',
    url(r'^$', login_required(HomeView.as_view()), name='home'),
    url(r'^add-current-urls/$', 'main.views.add_current_urls', name='add-current-urls'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
