# -*- coding: UTF-8 -*-
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils import timezone
from personas.models import Bombero


class NumeroOrden(models.Model):
    """
    Administrativamente siempre se usa el numero de orden de los bomberos en la carga de partes de siniestros.
    Los numeros de orden cambian de un bombero a otro con el tiempo debido a renuncias, ascensos, etc. con lo cual se
        debe tener registrado en que periodo de tiempo un bombero tuvo cada numero de orden por el que paso.
    El Número de Orden más bajo es asignado al Jefe del Cuerpo Activo y el más alto al de menor Jerarquía.
    Cuando entra un Bombero nuevo se le dá el Número de Orden más bajo hasta que el 02/06 siguiente se defina su
        situación respecto a su antigüedad, rango, etc. que pudiera tener dándole así el lugar que le corresponde.
    """
    numero_orden = models.SmallIntegerField(
        verbose_name=_("Número de Orden"))
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        related_name="numeros_orden_bombero")
    vigencia_desde = models.DateField(
        default=timezone.now)
    vigencia_hasta = models.DateField(
        null=True,
        blank=True)

    class Meta:
        verbose_name = _("Número de Orden")
        verbose_name_plural = _("Números de Orden")

    def __str__(self):
        return "{0} - {1} ({2})".format(
            self.numero_orden,
            self.bombero,
            self.vigencia)

    @receiver(post_save, sender=Bombero)
    def crear_nro_orden(sender, **kwargs):
        if kwargs.get('created', True):
            mayor = NumeroOrden.objects.filter(
                vigencia_hasta__isnull=True,
            ).order_by('-numero_orden').first()

            if mayor is not None:
                numero = mayor.numero_orden + 1
            else:
                numero = 1

            NumeroOrden.objects.create(
                bombero=kwargs.get('instance'),
                numero_orden=numero)

    @property
    def vigencia(self):
        vigencia = "vigente desde "
        if self.vigencia_hasta:
            vigencia += "{0} hasta el {1}".format(
                self.vigencia_desde,
                self.vigencia_hasta)
        else:
            vigencia += "{0}".format(
                self.vigencia_desde)
        return vigencia

    def cerrar_vigencia(self, fecha_cierre=timezone.now()):
        if not isinstance(fecha_cierre, datetime):
            try:
                fecha_cierre = datetime.strptime(fecha_cierre, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError(
                    {'vigencia_hasta':
                         _("La fecha de cierre de vigencia no es válida, debe tener el formato 'YYYY-MM-DD'.")})

        if self.vigencia_desde > fecha_cierre.date():
            raise ValidationError(
                {'vigencia_hasta':
                 _("La fecha de cierre de vigencia no debe ser mayor a la de inicio de la vigencia.")})
        self.vigencia_hasta = fecha_cierre
        self.save()

    def clean(self):
        numero = NumeroOrden.objects.filter(
            bombero=self.bombero,
            vigencia_desde__gte=self.vigencia_desde).count()
        if numero > 0 and self.id is None:
            raise ValidationError(
                {'vigencia_desde':
                 _("Ya existe un bombero con este número de orden vigente")})
