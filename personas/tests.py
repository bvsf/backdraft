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

        DireccionPostal.objects.create(
            persona = Persona.objects.get(apellido='Apellido'),
            uso = 'P',
            localidad = Localidad.objects.get(nombre='San Francisco'),
            calle = 'Algún Prócer',
            numero = '123',
        )
        DireccionPostal.objects.create(
            persona = Persona.objects.get(apellido='Apellido'),
            uso = 'L',
            localidad = Localidad.objects.get(nombre='San Francisco'),
            calle = 'Otro Prócer',
            numero = '456',
            piso = 'PA',
        )
        DireccionPostal.objects.create(
            persona = Persona.objects.get(apellido='Apellido'),
            uso = 'L',
            localidad = Localidad.objects.get(nombre='San Francisco'),
            calle = 'Una fecha importante',
            numero = '789',
            piso = '8vo.',
            departamento='A',
        )


    def test_model_Persona(self):
        persona = Persona.objects.get(apellido='Apellido')
        self.assertEqual(persona.nombre_completo, 'APELLIDO, Nombre')
        self.assertEqual(persona.edad, 25)
        self.assertEqual(persona.dni, 'D 12345678')
        self.assertEqual(persona.sangre, 'O (-)')
        self.assertEqual(persona.aniversario, None)

    def test_model_Localidad(self):
        provincia = Provincia.objects.get(nombre='Córdoba')
        self.assertEqual(provincia.__str__(), 'Córdoba (Arg.)')
        localidad = Localidad.objects.get(nombre='San Francisco')
        self.assertEqual(localidad.__str__(), 'San Francisco, Córdoba (Arg.)')
        self.assertEqual(localidad.nombre_completo, '(2400) San Francisco, Córdoba (Arg.)')

    def test_model_DireccionPostal(self):
        dirA = DireccionPostal.objects.get(calle='Algún Prócer')
        dirB = DireccionPostal.objects.get(calle='Otro Prócer')
        dirC = DireccionPostal.objects.get(calle='Una fecha importante')

        self.assertEqual(dirA.direccion_completa, 'Algún Prócer 123, San Francisco, Córdoba (Arg.)')
        self.assertEqual(dirB.direccion_completa, 'Otro Prócer 456 piso PA, San Francisco, Córdoba (Arg.)')
        self.assertEqual(dirC.direccion_completa, 'Una fecha importante 789 piso 8vo. dpto. "A", San Francisco, Córdoba (Arg.)')
