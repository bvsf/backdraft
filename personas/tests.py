from django.test import TestCase
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
        Persona.objects.create(
            apellido='Apellido',
            nombre='Nombre',
            documento='12345678',
            grupo_sanguineo='O',
            factor_sanguineo='-',
            fecha_nacimiento='1991-01-31',
            tipo_documento='DNI',
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
            entidad=Persona.objects.get(apellido='Apellido'),
            uso='P',
            localidad=Localidad.objects.get(nombre='San Francisco'),
            calle='Algún Prócer',
            numero='123',
        )
        DireccionPostal.objects.create(
            entidad=Persona.objects.get(apellido='Apellido'),
            uso='L',
            localidad=Localidad.objects.get(nombre='San Francisco'),
            calle='Otro Prócer',
            numero='456',
            piso='PA',
        )
        DireccionPostal.objects.create(
            entidad=Persona.objects.get(apellido='Apellido'),
            uso='L',
            localidad=Localidad.objects.get(nombre='San Francisco'),
            calle='Una fecha importante',
            numero='789',
            piso='8vo.',
            departamento='A',
        )

    def test_model_Persona(self):
        persona = Persona.objects.get(apellido='Apellido')
        self.assertEqual(persona.nombre_completo, 'APELLIDO, Nombre')
        self.assertEqual(persona.edad, 27)
        self.assertEqual(persona.dni, 'DNI 12345678')
        self.assertEqual(persona.sangre, 'O (-)')
        self.assertEqual(persona.aniversario, None)

    def test_model_Localidad(self):
        provincia = Provincia.objects.get(nombre='Córdoba')
        self.assertEqual(provincia.__str__(), 'Córdoba (Arg.)')
        localidad = Localidad.objects.get(nombre='San Francisco')
        self.assertEqual(localidad.__str__(), 'San Francisco, Córdoba (Arg.)')
        self.assertEqual(localidad.nombre_completo, '(2400) San Francisco, Córdoba (Arg.)')

    def test_model_DireccionPostal(self):
        dir_a = DireccionPostal.objects.get(calle='Algún Prócer')
        dir_b = DireccionPostal.objects.get(calle='Otro Prócer')
        dir_c = DireccionPostal.objects.get(calle='Una fecha importante')

        self.assertEqual(dir_a.direccion_completa, 'Algún Prócer 123, San Francisco, Córdoba (Arg.)')
        self.assertEqual(dir_b.direccion_completa, 'Otro Prócer 456 piso PA, San Francisco, Córdoba (Arg.)')
        self.assertEqual(dir_c.direccion_completa, 'Una fecha importante 789 piso 8vo. dpto. "A", San Francisco, '
                                                   'Córdoba (Arg.)')
