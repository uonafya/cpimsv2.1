"""OVC care section urls."""
from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'cpovc_ovc.views',
    url(r'^$', 'ovc_home', name='ovc_home'),
    url(r'^search/$', 'ovc_search', name='ovc_search'),
    url(r'^register/(?P<id>\d+)/$',
        'ovc_register', name='ovc_register'),
    url(r'^edit/(?P<id>\d+)/$',
        'ovc_edit', name='ovc_edit'),
    url(r'^view/(?P<id>\d+)/$',
        'ovc_view', name='ovc_view'),
    url(r'^hh/(?P<hhid>[0-9A-Za-z_\-]+)/$',
        'hh_manage', name='hh_manage'),)
