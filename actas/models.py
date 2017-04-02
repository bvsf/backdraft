from django.db import models


class Acta (models.Model):
    numero_acta = models.CharField(
        max_length=100,
        verbose_name=_('Numero de Acta'),
        unique=True)
    fecha_acta = models.DateField(
        verbose_name=_('Fecha de Acta'),
    )
# Create your models here.
