from django.conf.urls import patterns, url

# This should contain urls related to auth app ONLY
urlpatterns = patterns('cpovc_auth.views',
                       url(r'^$', 'home'),
                       url(r'^register/$', 'register'),
                       )
