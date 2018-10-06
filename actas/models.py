# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone


def get_last_libro():
    acta = Acta.objects.all().order_by('-numero_libro').first()
    if not acta:
        return 1
    else:
        return acta.numero_libro


def get_last_folio():
    acta = Acta.objects.filter(
        numero_libro=get_last_libro()
    ).order_by('-numero_folio').first()
    if not acta:
        return 1
    else:
        return acta.numero_folio


def get_next_acta():
    acta = Acta.objects.filter(
        numero_libro=get_last_libro(),
        numero_folio=get_last_folio()
    ).order_by('-numero_acta').first()
    if not acta:
        return 1
    else:
        return acta.numero_acta + 1


class Acta(models.Model):
    numero_libro = models.SmallIntegerField(
        default=get_last_libro,
        verbose_name=_("Número de Libro"))
    numero_folio = models.SmallIntegerField(
        default=get_last_folio,
        verbose_name=_("Número de Folio"))
    numero_acta = models.SmallIntegerField(
        default=get_next_acta,
        verbose_name=_("Número de Acta"))
    fecha_acta = models.DateField(
        verbose_name=_("Fecha de Acta"),
        default=timezone.now)
    descripcion_acta = models.TextField(
        verbose_name=_("Descripción del Acta"),
        max_length=1000)

    @property
    def nombre_completo(self):
        return _("Libro: {0} Folio: {1} Acta: {2} - Fecha: {3}").format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
            self.fecha_acta,
        )

    @property
    def nombre_corto(self):
        return _("L.{0} / F.{1} / A.{2}").format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
        )

    class Meta:
        unique_together = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
        )
        ordering = [
            'numero_libro',
            'numero_folio',
            'numero_acta',
        ]

    def __str__(self):
        return "{0}".format(self.nombre_completo)


