from django.conf.urls import url
from django.contrib import admin

from personas.api.views import (
	PersonaListAPIView,
	BomberoListAPIView,
	BomberoDetailAPIView,
	BomberoUpdateAPIView,
	)

urlpatterns = [
	url(r'^$', BomberoListAPIView.as_view(), name='firefighter-list'),
	url(r'^$', BomberoDetailAPIView.as_view(), name='firefighter'),
	url(r'^$', PersonaListAPIView.as_view(), name='people-list'),
	
]