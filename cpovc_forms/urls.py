from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns('cpovc_forms.views',
                       url(r'^$', 'forms_home', name='forms'),
                       url(r'^case_record_sheet/(?P<formtype>\d+)/$', 'case_record_sheet',
                           name='case_record_sheet'),
                       url(r'^ovc_search/$', 'ovc_search', name='ovc_search'),
                       url(r'^registry/$', 'forms_home', name='forms_registry'),
                       )
