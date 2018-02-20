from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    )

from personas.models import (
    Bombero,
    Persona,
    DireccionWeb,
    )

from nro_orden.models import (
    NumeroOrden,
    )

from personas.api.serializers import (
    BomberoSerializer,
    PersonaSerializer,
    NumeroOrdenSerializer,
    DireccionWebSerializer,
    )


class PersonaListAPIView(ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class BomberoListAPIView(ListAPIView):
    queryset = Bombero.objects.all()
    serializer_class = BomberoSerializer

    #def get_queryset()


class BomberoDetailAPIView(RetrieveAPIView):
    queryset = Bombero.objects.all()
    serializer_class = BomberoSerializer
    lookup_field = 'pk'


class BomberoUpdateAPIView(UpdateAPIView):
    queryset = Bombero.objects.all()
    serializer_class = BomberoSerializer
    lookup_field = 'pk'


class NumeroOrdenListAPIView(ListAPIView):
    queryset = NumeroOrden.objects.all()
    serializer_class = NumeroOrdenSerializer


class DireccionWebListAPIView(ListAPIView):
    queryset = DireccionWeb.objects.all()
    serializer_class = DireccionWebSerializer
