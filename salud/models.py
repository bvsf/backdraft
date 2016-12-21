# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from personas.models import Bombero

class Alergenos(models.Model):
    nombre_alergeno = models.CharField(
        max_length=255,
        verbose_name=_('Nombre del Alérgeno'),
    )


class Alergicos(models.Model):
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero")
    )
    alergeno = models.ForeignKey(
        Alergenos,
        verbose_name=_("Alérgeno")
    )
    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Obervaciones"),
        blank=True,
        null=True
    )