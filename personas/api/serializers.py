from rest_framework import serializers

from personas.models import Bombero, Persona, NumeroOrden, DireccionWeb
from localidades.models import Localidad
from localidades.api.serializers import LocalidadSerializer

class PersonaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Persona
		fields = [
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


class BomberoSerializer(serializers.ModelSerializer):
	persona = PersonaSerializer(read_only=True)
	lugar_nacimiento = LocalidadSerializer()
	numero_orden_bombero = NumeroOrdenSerializer(many=True, read_only=True)
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


class DireccionWebSerializer(serializers.ModelSerializer):
	class Meta:
		model = DireccionWeb
		fields= [
			'direccion',
			'tipo',
		]
