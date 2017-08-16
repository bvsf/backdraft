from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from personas.models import Bombero


class Acta(models.Model):
    numero_libro = models.CharField(
        max_length=10,
        verbose_name=_("Número de Libro"))
    numero_folio = models.CharField(
        max_length=10,
        verbose_name=_("Número de Folio"),
        unique=True)
    numero_acta = models.CharField(
        max_length=10,
        verbose_name=_("Número de Acta"),
        unique=True)
    fecha_acta = models.DateField(
        verbose_name=_("Fecha de Acta"),
        default=timezone.now)
    descripcion_acta = models.CharField(
        verbose_name=_("Descripción del Acta"),
        max_length=1000)

    class Meta:
        abstract = True

    @property
    def nombre_completo(self):
        return _("Libro: {0} Folio: {1} Acta: {2} - Fecha:").format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
            self.fecha_acta)

    @property
    def nombre_corto(self):
        return _("L.{0} / F.{1} / A.{2}").format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
        )

    def __str__(self):
        return "{0}".format(self.nombre_completo)


class Licencia(Acta):
    fecha_desde = models.DateField(
        verbose_name=_("Fecha desde")
    )
    fecha_hasta = models.DateField(
        verbose_name=_("Fecha hasta")
    )
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero")
    )

    def __str__(self):
        return _("({0}) - Licencia desde {1} hasta {2}").format(
            self.nombre_corto,
            self.fecha_acta,
            self.fecha_hasta)

    @property
    def periodo_licencia(self):
        return _("Desde: {0} hasta: {1}").format(
            self.fecha_desde,
            self.fecha_hasta,
        )