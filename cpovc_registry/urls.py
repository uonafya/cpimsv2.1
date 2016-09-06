"""Registry section urls."""
from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'cpovc_registry.views',
    url(r'^$', 'home', name='registry'),
    url(r'^new/$', 'register_new', name='registry_new'),
    url(r'^(?P<org_id>\d+)/$', 'register_details'),
    url(r'^edit/(?P<org_id>\d+)/$', 'register_edit', name='registry_edit'),
    url(r'^persons_search/$', 'persons_search', name='search_persons'),
    url(r'^new_user/(?P<id>\d+)/$', 'new_user', name='new_user'),
    url(r'^person/$', 'person_actions', name='person_actions'),
    url(r'^new_person/$', 'new_person', name='new_person'),
    url(r'^edit_person/(?P<id>\d+)/$', 'edit_person', name='edit_person'),
    url(r'^view_person/(?P<id>\d+)/$', 'view_person', name='view_person'),
    url(r'^delete_person/(?P<id>\d+)/$', 'delete_person',
        name='delete_person'),
    url(r'^lookup/$', 'registry_look', name='reg_lookup'), )
# {% url 'view_person' id=result.id %}
