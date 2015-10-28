"""
cpims URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cpims.views.home', name='home'),
    url(r'^login/$', 'cpovc_auth.views.log_in', name='login'),
    url(r'^register/$', 'cpovc_auth.views.register', name='register'),
]

handler400 = 'cpims.views.handler_400'
handler404 = 'cpims.views.handler_404'
handler500 = 'cpims.views.handler_500'
