from django.conf.urls import patterns, include, url
from dmodels.views import create, show, models_list
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/', create),
    url(r'^$', create),
    url(r'^models_list/', models_list),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
