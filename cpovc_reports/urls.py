"""Urls for reports."""
from django.conf.urls import patterns, url

# This should contain urls related to reports ONLY
urlpatterns = patterns('cpovc_reports.views',
                       url(r'^$', 'reports_home', name='reports'),
                       url(r'^documents/$', 'reports_home',
                           name='document_reports'),
                       url(r'^(?P<id>\d+)/$', 'reports_cpims',
                           name='cpims_reports'),
                       url(r'^caseload/$', 'reports_caseload',
                           name='caseload_reports'),
                       url(r'^manage/$', 'manage_reports',
                           name='manage_reports'),
                       url(r'^download/(?P<file_name>[0-9A-Za-z_\.=\- ]+)$',
                           'reports_download', name='download_reports'),
                       url(r'^generate/$', 'reports_generate',
                           name='generate_reports')
                       )
