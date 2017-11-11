from django.conf.urls import url
from django.contrib import admin

from personas.api.views import (
	PersonaListAPIView,
	BomberoListAPIView,
	BomberoDetailAPIView,
	BomberoUpdateAPIView,
	)

urlpatterns = [
	url(r'^listado/bomberos$', BomberoListAPIView.as_view(), name='firefighter-list'),
	url(r'^detalle/bombero/$', BomberoDetailAPIView.as_view(), name='firefighter'),
	url(r'^listado/personas$', PersonaListAPIView.as_view(), name='people-list'),
	
]