from django.conf.urls import url
from django.contrib import admin

from personas.api.views import (
	BomberoListAPIView,
	PersonaListAPIView,
	BomberoDetailAPIView,
	BomberoUpdateAPIView
	)

urlpatterns = [
	url(r'^$', BomberoListAPIView.as_view(), name='firefighter-list'),
	url(r'^$', PersonaListAPIView.as_view(), name='people-list'),
	
]