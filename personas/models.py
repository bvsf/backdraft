# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from tipos_documento.models import TipoDocumento
from datetime import date
from .choices import (
    GRUPO_SANGUINEO,
    FACTOR_SANGUINEO)


class Registrado(models.Model):
    borrado = models.BooleanField(default=False)
    historico = models.BooleanField(default=False)
    usuario_creador = models.ForeignKey(
        User,
        related_name='persona_creator',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField(
         auto_now_add=True)
    usuario_modificador = models.ForeignKey(
        User,
        related_name='persona_updater',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    fecha_modificacion = models.DateTimeField(
        auto_now=True)


class Persona(Registrado):
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
    fecha_nacimiento = models.DateField(
        verbose_name=_('Fecha de Nacimiento'))

    @property
    def nombre_completo(self):
        return "{0}, {1}".format(
            self.apellido.upper(),
            self.nombre)

    @property
    def edad(self):
        delta = date.today() . self.fecha_nacimiento
        return int((delta.days / (365.2425)))

    @property
    def dni(self):
        return "{0} {1}".format(
            self.tipo_documento,
            self.documento)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
