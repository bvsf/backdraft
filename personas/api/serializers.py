from rest_framework import serializers

from personas.models import (
    Entidad,
    Bombero,
    Persona,
    Medio,
    DireccionPostal,
    DireccionWeb,
)

from nro_orden.models import (
    NumeroOrden,
    )

from localidades.api.serializers import LocalidadSerializer


class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = [
            'tipo_cuit',
            'nro_cuit',
        ]


class PersonaSerializer(EntidadSerializer):
    class Meta(EntidadSerializer.Meta):
        model = Persona
        fields = EntidadSerializer.Meta.fields + [
            'nombre',
            'apellido',
            'documento',
            'fecha_nacimiento',
        ]


class NumeroOrdenSerializer(serializers.ModelSerializer):
    #bombero = serializers.RelatedField(source='bombero', read_only=True)

    class Meta:
        model = NumeroOrden
        fields = [
            'numero_orden',
            'vigencia_desde',
            'vigencia_hasta',
        ]


class MedioSerializer(serializers.ModelSerializer):
    medio_entidad = EntidadSerializer(read_only=True)

    class Meta:
        models = Medio
        fields = [
            'medio_entidad',
            'uso',
            'observaciones',
        ]


class DireccionPostalSerializer(serializers.ModelSerializer):
    localidad = LocalidadSerializer()

    class Meta:
        model = DireccionPostal
        fields = [
            'localidad',
            'calle',
            'numero',
            'piso',
            'departamento',
        ]


class DireccionWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionWeb
        fields= [
            'direccion',
            'tipo',
        ]


class BomberoSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(
        read_only=True,
    )
    lugar_nacimiento = LocalidadSerializer()
    numero_orden_bombero = NumeroOrdenSerializer(
        many=True,
        read_only=True,
    )
    #lugar_nacimiento = serializers.RelatedField(source='lugar_nacimiento.codigo_postal', queryset=Localidad.objects.all())
    class Meta:
        model = Bombero
        fields = [
            'id',
            'persona',
            'lugar_nacimiento',
            'numero_credencial',
            'fecha_vencimiento',
            'estado_civil',
            'numero_orden_bombero',
        ]
