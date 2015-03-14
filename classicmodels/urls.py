from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'classicmodels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',include('classic_models.urls')),
    url(r'^classic_models/',include('classic_models.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
