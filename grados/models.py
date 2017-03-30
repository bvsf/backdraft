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
    excepcion = models.BooleanField(
        verbose_name=_('Posee más de un grado superior'),
        default=False,
        null=False,
        blank=False
    )

    def __str__(self):
        return "{0} - {1}".format(
            self.nombre,
            self.escalafon)

    def grado_superior_del_superior(self):
        '''Trata las excepciones de los grados especiales.'''
        if (self.excepcion is True):
            grado = self.grado_superior
            return grado.grado_superior
        else:
            if (self.grado_superior is None):
                return _('Éste grado no posee grado superior')
            else:
                return _(
                    'El grado superior de éste grado no posee grado superior')