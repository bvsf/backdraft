# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from tipos_documento.models import TipoDocumento
from datetime import date
from .choices import (
    GRUPO_SANGUINEO,
    FACTOR_SANGUINEO)


class Persona(models.Model):
    apellido = models.CharField(
        max_length=255,
        verbose_name=_('Apellido'))
    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre'))
    tipo_documento = models.ForeignKey(TipoDocumento)
    documento = models.CharField(
        max_length=11,
        verbose_name=_('Número de documento'))
    grupo_sanguineo = models.CharField(
        max_length=255,
        choices=GRUPO_SANGUINEO,
        verbose_name=_("Grupo Sanguíneo"))
    factor_sanguineo = models.CharField(
        max_length=255,
        choices=FACTOR_SANGUINEO,
        verbose_name=_("Factor Sanguíneo"))
    fecha_nacimiento = models.DateField(
        verbose_name=_('Fecha de Nacimiento'))

    @property
    def nombre_completo(self):
        return "{0}, {1}".format(
            self.apellido.upper(),
            self.nombre)

    @property
    def edad(self):
        delta = (date.today() - self.fecha_nacimiento)
        return int((delta.days / (365.2425)))

    @property
    def dni(self):
        return "{0} {1}".format(
            self.tipo_documento,
            self.documento)

    @property
    def sangre(self):
        return "{0}{1}".format(
            self.grupo_sanguineo,
            self.factor_sanguineo)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
