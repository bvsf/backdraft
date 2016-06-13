# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from tipos_documento.models import TipoDocumento
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
    fecha_nacimiento = models.DateField(
        verbose_name=_('Fecha de Nacimiento'))
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

