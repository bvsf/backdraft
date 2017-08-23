from rest_framework import serializers

from personas.models import Bombero, Persona
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


class BomberoSerializer(serializers.ModelSerializer):
	persona = PersonaSerializer(read_only=True)
	lugar_nacimiento = LocalidadSerializer()
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
		]