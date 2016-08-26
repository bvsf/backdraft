from django.test import TestCase
from tipos_documento.models import TipoDocumento
from personas.models import (
    Persona,
    Bombero,
    DireccionPostal)


class SimpleTest(TestCase):

    def setUp(self):

        TipoDocumento.objects.create(
            tipo='Documento',
            abreviatura='D')

        Persona.objects.create(
            apellido='Apellido',
            nombre='Nombre',
            documento='12345678',
            grupo_sanguineo='O',
            factor_sanguineo='RH-',
            fecha_nacimiento='1991-01-31',
            tipo_documento=TipoDocumento.objects.get(abreviatura='D'))


    def test_persona_nombre_completo(self):
        persona1 = Persona.objects.get(apellido='Apellido')
        self.assertEqual(persona1.dni, 'D 12345678')
        self.assertEqual(persona1.edad, 25)
        self.assertEqual(persona1.nombre_completo, 'APELLIDO, Nombre')
        self.assertEqual(persona1.aniversario, None)
