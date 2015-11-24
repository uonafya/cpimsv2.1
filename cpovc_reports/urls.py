from django.conf.urls import patterns, url

# This should contain urls related to reports ONLY
urlpatterns = patterns('cpovc_reports.views',
                       url(r'^$', 'reports_home', name='reports'),
                       url(r'^registry/$', 'reports_home',
                           name='reports_registry')
                       )
