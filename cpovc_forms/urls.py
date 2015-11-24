from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns('cpovc_forms.views',
                       url(r'^$', 'forms_home', name='forms'),
                       url(r'^registry/$', 'forms_home', name='forms_registry')
                       )
