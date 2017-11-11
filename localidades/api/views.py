from rest_framework.generics import ListAPIView, RetrieveAPIView

from localidades.models import Zona, Localidad, Provincia
from localidades.api.serializers import LocalidadSerializer, ProvinciaSerializer

'''
class ZonaListAPIView(ListAPIView):
    queryset = Zona.objects.all()
    serializer_class = BomberoSerializer

    #def get_queryset()
'''

class LocalidadListAPIView(ListAPIView):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer


class ProvinciaListAPIView(ListAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class LocalidadDetailAPIView(RetrieveAPIView):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer
    lookup_field = 'pk'

class ProvinciaDetailAPIView(RetrieveAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    lookup_field = 'pk'