from django.conf.urls import url
from .api import SetupListView

api_urls = [
    url(r'^setuplists/$',
        SetupListView.as_view(),
        name='setup-list-view'),
]