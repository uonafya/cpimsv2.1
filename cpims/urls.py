"""
cpims URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from cpovc_auth import urls as auth_urls
from cpovc_registry import urls as registry_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cpims.views.home', name='home'),
    url(r'^login/$', 'cpovc_auth.views.log_in', name='login'),
    url(r'^logout/$', 'cpovc_auth.views.log_out', name='logout'),
    url(r'^register/$', 'cpovc_auth.views.register', name='register'),
    url(r'^auth/$', include(auth_urls)),
    url(r'^registry/', include(registry_urls))
]

handler400 = 'cpims.views.handler_400'
handler404 = 'cpims.views.handler_404'
handler500 = 'cpims.views.handler_500'
