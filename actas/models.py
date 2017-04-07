from django.db import models
from django.utils.translation import ugettext as _

class Acta (models.Model):

    fecha_acta = models.DateField(
        verbose_name=('Fecha de Acta'),
    )
    numero_acta = models.CharField(
        max_length=100,
        verbose_name=_('Numero de Acta'),
        unique=True)
    numero_folio = models.CharField(
        max_length=100,
        verbose_name=_('Numero de Folio'),
        unique=True,
    )
    numero_libro = models.CharField(
        max_length=100,
        verbose_name=_('Numero de Libro'),
    )
    descripcion_acta = models.CharField(
        verbose_name=_('Descripcion del Acta'),
        max_length = 1000,
    )
class Meta:
       abstract = True
# Create your models here.
