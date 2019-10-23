from rest_framework import serializers

from localidades.models import (
    Zona,
    Localidad,
    Provincia,
    Pais,
)


class ZonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zona
        fields = (
            'nombre',
            'abreviatura',
        )


class LocalidadSerializer(serializers.ModelSerializer):
    provincia_nombre = serializers.PrimaryKeyRelatedField(
        queryset=Provincia.objects.all(),
        source='provincia.nombre'
    )
    provincia_abreviatura = serializers.PrimaryKeyRelatedField(
        queryset=Provincia.objects.all(),
        source='provincia.abreviatura',
    )

    class Meta:
        model = Localidad
        fields = (
            'nombre',
            'abreviatura',
            'codigo_postal',
            'provincia_nombre',
            'provincia_abreviatura',
        )


class ProvinciaSerializer(serializers.ModelSerializer):
    provincia = LocalidadSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Provincia
        fields = (
            'nombre',
            'abreviatura',
            'provincia',
        )
