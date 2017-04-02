from django.db import models


class Acta (models.Model):

    fecha_acta = models.DateField(
        verbose_name=_('Fecha de Acta'),
    )
    numero_acta = models.CharField(
        max_length=100,
        verbose_name=_('Numero de Acta'),
        unique=True)
    numero_folio = models.CharField(
        verbose_name=_ ('Numero de Folio'),
        unique=True,
    )
    numero_libro = models.CharField(
        verbose_name=_('Numero de Libro'),
    )
    descripcion_acta =_('Descripcion del Acta')
# Create your models here.
