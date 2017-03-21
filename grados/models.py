# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Rango(models.Model):

    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre')
    )
    color = models.CharField(
        max_length=255,
        verbose_name=_('Color')
    )

    def __str__(self):
        return self.nombre


class Escalafon(models.Model):

    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre')
    )
    rango = models.ForeignKey(
        Rango,
        verbose_name=_('Rango')
    )

    def __str__(self):
        return "{0} ({1})".format(
            self.nombre,
            self.rango)


class Grados(models.Model):

    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre')
    )
    grado_superior = models.OneToOneField(
        'self',
        blank=True,
        null=True,
        verbose_name=_('Grado Superior')
    )
    escalafon = models.ForeignKey(
        Escalafon,
        verbose_name=_('Escalafón')
    )

    def __str__(self):
        return "{0} - {1}".format(
            self.nombre,
            self.escalafon)
#TODO: Hacer función que permita saltar los grados especiales.
#Antes de guardar el ascenso, verificar si se puede hacer
#(llamada desde Ascenso). Agregar forma de identificar excepciones.
#Si existe grado superior de ese grado, proseguir
#Si no existe grado superior de ese grado, salir
#Si existe la excepción, tener el cuenta el grado superior del grado superior
#Si no existe la excepcion, verificar si el grado superior conincide el ascenso
