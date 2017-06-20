from django.db import models
from django.utils.translation import ugettext as _


class Acta(models.Model):
    numero_libro = models.CharField(
        max_length=10,
        verbose_name=_("Numero de Libro"))
    numero_folio = models.CharField(
        max_length=10,
        verbose_name=_("Numero de Folio"),
        unique=True)
    numero_acta = models.CharField(
        max_length=10,
        verbose_name=_("Numero de Acta"),
        unique=True)
    fecha_acta = models.DateField(
        verbose_name=_("Fecha de Acta"),)
    descripcion_acta = models.CharField(
        verbose_name=_("Descripcion del Acta"),
        max_length=1000)

    class Meta:
           abstract = True

    def __str__(self):
        return "Libro: {0} Folio: {1} Acta: {2} - Fecha:".format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
            self.fecha_acta)
