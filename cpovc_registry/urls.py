from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns('cpovc_registry.views',
                       url(r'^$', 'home', name='registry'),
                       url(r'^new/$', 'register_new', name='registry/new'),
                       url(r'^(?P<org_id>\d+)/$', 'register_details'),
                       url(r'^edit/(?P<org_id>\d+)/$', 'register_edit'),
                       url(r'^persons_search/$', 'persons_search',
                           name='search_persons'),
                       url(r'^workforce_search/$', 'workforce_search',
                           name='workforce_search'),
                       url(r'^new_user/$', 'new_user', name='new_user'),
                       url(r'^new_person/$', 'new_person', name='new_person'),
                       )
