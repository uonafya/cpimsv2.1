"""Urls for reports."""
from django.conf.urls import patterns, url

# This should contain urls related to reports ONLY
urlpatterns = patterns('cpovc_gis.views',
                       url(r'^$', 'gis_home', name='gis_home'),
                       )
