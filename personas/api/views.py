from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView

from personas.models import Bombero, Persona
from personas.api.serializers import BomberoSerializer, PersonaSerializer


class BomberoListAPIView(ListAPIView):
	queryset = Bombero.objects.all()
	serializer_class = BomberoSerializer

	#def get_queryset()


class PersonaListAPIView(ListAPIView):
	queryset = Persona.objects.all()
	serializer_class = PersonaSerializer


class BomberoDetailAPIView(RetrieveAPIView):
	queryset = Bombero.objects.all()
	serializer_class = BomberoSerializer
	lookup_field = 'pk'

class BomberoUpdateAPIView(UpdateAPIView):
	queryset = Bombero.objects.all()
	serializer_class = BomberoSerializer
	lookup_field = 'pk'
