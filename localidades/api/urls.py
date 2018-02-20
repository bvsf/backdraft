from django.conf.urls import url
from django.contrib import admin

from localidades.api.views import (
    LocalidadListAPIView,
    ProvinciaListAPIView,
    LocalidadDetailAPIView,
    ProvinciaDetailAPIView
    )

urlpatterns = [
    #url(r'^$', ZonaSerializer.as_view(), name='zona-view'),
    url(r'^$', LocalidadListAPIView.as_view(), name='localidad-view'),
    url(r'^provincias/$', ProvinciaListAPIView.as_view(), name='provincia-view'),
    url(r'^(?P<pk>[\w-]+)$', LocalidadDetailAPIView.as_view(), name='localidad-detail'),
    url(r'^provincias/(?P<pk>[\w-]+)$', ProvinciaDetailAPIView.as_view(), name='provincia-detail'),
]