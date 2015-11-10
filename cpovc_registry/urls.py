from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns('cpovc_registry.views',
                       url(r'^$', 'home', name='registry'),
                       url(r'^new/$', 'register_new', name='registry/new'),
                       url(r'^(?P<org_id>\d+)/$', 'register_details'),
                       url(r'^edit/(?P<org_id>\d+)/$', 'register_edit'),
                       )
