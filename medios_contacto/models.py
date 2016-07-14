from django.db import models
from django.utils.translation import ugettext as _
from localidades.models import Localidad


class Medio(models.Model):
    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Obervaciones"),
        blank=True,
        null=True)

    class Meta:
        abstract = True


class DireccionPostal(Medio):
    localidad = models.ForeignKey(
        Localidad,
        verbose_name=_("Localidad"))
    calle = models.CharField(
        max_length=255,
        verbose_name=_("Calle"))
    numero = models.IntegerField(
        verbose_name=_("Número"))
    piso = models.CharField(
        max_length=5,
        verbose_name=_("Piso"),
        blank=True,
        null=True)
    departamento = models.CharField(
        max_length=5,
        verbose_name=_("Departamento"),
        blank=True,
        null=True)

    @property
    def direccion_completa(self):
        piso = ""
        dpto = ""
        if self.piso:
            piso = " piso {0}".format(self.piso)
        if self.departamento:
            dpto = ' dpto. "{0}"'.format(self.departamento)

        return "{0} {1}{2}{3}, {4}".format(
            self.calle,
            self.numero,
            piso,
            dpto,
            self.localidad)

    def __str__(self):
        return "{0} {1} {2} {3}".format(
            self.calle,
            self.numero,
            self.piso,
            self.departamento)

    class Meta:
        verbose_name = _("Dirección Postal")
        verbose_name_plural = _("Direcciones Postales")
