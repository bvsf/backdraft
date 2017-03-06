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
    rango = models.ForeignFey(
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
        Grados,
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
