from django.conf.urls import url
from .api import SetupListView, SetupListChildView

api_urls = [
    url(r'^setuplists/$',
        SetupListView.as_view(),
        name='setup-list-view'),
    url(r'^setuplists/children/$',
        SetupListChildView.as_view(),
        name='setup-list-child-view'),
]