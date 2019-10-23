# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class Zona(models.Model):
    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre'))
    abreviatura = models.CharField(
        max_length=255,
        verbose_name=_('Abreviatura'),
        blank=True,
        null=True)

    def __str__(self):
        return "{0}".format(self.nombre)

    class Meta:
        abstract = True


class Pais(Zona):
    class Meta:
        ordering = ['nombre']
        verbose_name = _("Pais")
        verbose_name_plural = _("Paises")


class Provincia(Zona):
    pais = models.ForeignKey(
        Pais,
        verbose_name=_("Pais"),
        related_name='pais',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return "{0} ({1})".format(
            self.nombre,
            self.pais.abreviatura)

    class Meta:
        ordering = ['pais', 'nombre']
        verbose_name = _("Provincia")
        verbose_name_plural = _("Provincias")


class Localidad(Zona):
    provincia = models.ForeignKey(
        Provincia,
        verbose_name=_("Provincia"),
        related_name='provincia',
        on_delete=models.PROTECT,
    )
    codigo_postal = models.CharField(
        max_length=255,
        verbose_name=_("Codigo Postal"))

    def __str__(self):
        return "{0}, {1}".format(
            self.nombre,
            self.provincia)

    @property
    def nombre_completo(self):
        return "({0}) {1}, {2}".format(
            self.codigo_postal,
            self.nombre,
            self.provincia)

    class Meta:
        ordering = ['provincia', 'nombre']
        verbose_name = _("Localidad")
        verbose_name_plural = _("Localidades")
