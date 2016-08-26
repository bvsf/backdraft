from django.test import TestCase
from tipos_documento.models import TipoDocumento
from localidades.models import (
    Localidad,
    Provincia,
    Pais)
from personas.models import (
    Persona,
    Bombero,
    DireccionPostal)


class SimpleTest(TestCase):

    def setUp(self):
        TipoDocumento.objects.create(
            tipo='Documento',
            abreviatura='D',
        )

        Persona.objects.create(
            apellido='Apellido',
            nombre='Nombre',
            documento='12345678',
            grupo_sanguineo='O',
            factor_sanguineo='-',
            fecha_nacimiento='1991-01-31',
            tipo_documento=TipoDocumento.objects.get(abreviatura='D'),
        )

        Pais.objects.create(
            nombre='Argentina',
            abreviatura='Arg.',
        )

        Provincia.objects.create(
            nombre='Córdoba',
            abreviatura='Cba.',
            pais=Pais.objects.get(nombre='Argentina'),
        )

        Localidad.objects.create(
            nombre='San Francisco',
            abreviatura='San Fco.',
            codigo_postal='2400',
            provincia=Provincia.objects.get(nombre='Córdoba'),
        )


    def test_model_persona(self):
        persona = Persona.objects.get(apellido='Apellido')
        self.assertEqual(persona.nombre_completo, 'APELLIDO, Nombre')
        self.assertEqual(persona.edad, 25)
        self.assertEqual(persona.dni, 'D 12345678')
        self.assertEqual(persona.sangre, 'O (-)')
        self.assertEqual(persona.aniversario, None)

    def test_model_localidad(self):
        provincia = Provincia.objects.get(nombre='Córdoba')
        self.assertEqual(provincia.__str__(), 'Córdoba (Arg.)')
        localidad = Localidad.objects.get(nombre='San Francisco')
        self.assertEqual(localidad.__str__(), 'San Francisco, Córdoba (Arg.)')
        self.assertEqual(localidad.nombre_completo, '(2400) San Francisco, Córdoba (Arg.)')

