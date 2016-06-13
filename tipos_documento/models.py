from django.db import models
from django.utils.translation import ugettext as _


class TipoDocumento(models.Model):
    tipo = models.CharField(
        max_length=255,
        verbose_name=_('Tipo de Documento'))
    abreviatura = models.CharField(
        max_length=10,
        verbose_name=_('Abreviatura'))

    def __str__(self):
        return "{0}".format(self.abreviatura)

    class Meta:
        verbose_name = _('Tipo de Documento')
        verbose_name_plural = _('Tipos de Documento')
        ordering = ['abreviatura', 'tipo']
