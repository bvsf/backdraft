from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from personas.models import (
    Bombero,
    Institucion,
)
from grados.models import Grado
from .choices import (
    TIPO_SANCION,
)


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

    @property
    def nombre_completo(self):
        return _("Libro: {0} Folio: {1} Acta: {2} - Fecha: {3}").format(
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
    motivo = models.CharField(
        max_length=500,
        verbose_name=_("Motivo de la Licencia")
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_licenciado',
        verbose_name=_("Bombero")
    )

    def __str__(self):
        return _("({0}) - Licencia desde {1} hasta {2}").format(
            self.nombre_corto,
            self.fecha_acta,
            self.fecha_hasta,
        )

    @property
    def periodo_licencia(self):
        return _("Desde: {0} hasta: {1}").format(
            self.fecha_desde,
            self.fecha_hasta,
        )

    class Meta:
        verbose_name = _("Acta de Licencia")
        verbose_name_plural = _("Actas de Licencias")


class ActaAscenso(Acta):
    fecha_efectiva = models.DateField(
        verbose_name=_("Fecha efectiva de Ascenso")
    )

    class Meta:
        verbose_name = _("Acta de Ascenso")
        verbose_name_plural = _("Actas de Ascensos")


class Ascenso(models.Model):
    acta_ascenso = models.ForeignKey(
        ActaAscenso,
        related_name='acta_ascenso',
        verbose_name=_("Acta de Ascenso"),
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_ascendido',
        verbose_name=_("Bombero Ascendido"),
    )
    grado_ascenso = models.ForeignKey(
        Grado,
        related_name='grado_ascendido',
        verbose_name=_("Grado Ascendido"),
    )

    def __str__(self):
        return _("{0} ascendido a {1} el {2}").format(
            self.bombero,
            self.grado_ascenso,
            self.acta_ascenso.fecha_efectiva,
        )

    class Meta:
        ordering = ['acta_ascenso']


class ActaSancion(Acta):
    fecha_incidente = models.DateField(
        verbose_name=_("Fecha del Incidente"),
    )
    descripcion_incidente = models.CharField(
        max_length=500,
        verbose_name=_("Descripción del Incidente"),
    )

    def get_sanciones(self):
        return Sancion.objects.filter(acta_sancion=self)

    class Meta:
        verbose_name = _("Acta de Sanción")
        verbose_name_plural = _("Actas de Sanciones")


class Sancion(models.Model):
    acta_sancion = models.ForeignKey(
        ActaSancion,
        related_name='acta_sancion',
        verbose_name=_("Acta de Sanción"),
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_interviniente',
        verbose_name=_("Bombero interviniente"),
    )
    rol_incidente = models.CharField(
        max_length=1000,
        verbose_name=_("Rol que cumplió en el incidente"),
    )
    descargo = models.TextField(
        blank=True,
        null=True,
        max_length=2000,
        verbose_name=_("Descargo presentado por el Bombero"),
    )
    tipo_sancion = models.CharField(
        max_length=20,
        choices=TIPO_SANCION,
        default=TIPO_SANCION[0][0],
        verbose_name=_("Tipo de Sanción disciplinaria"),
    )
    dias_suspencion = models.SmallIntegerField(
        default=0,
        verbose_name=_("Días de Suspención"),
    )
    fecha_efectiva = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Fecha en que se efectiviza la sanción"),
    )

    def __str__(self):
        linea = "{0} {1} {2}".format(
            self.acta_sancion.nombre_corto,
            self.bombero,
            self.tipo_sancion)

        if self.dias_suspencion>0:
            linea += _("Suspendido {0} días").format(self.dias_suspencion)

        return linea

    class Meta:
        ordering = ['acta_sancion']


class Premio(Acta):
    fecha_premiacion = models.DateField(
        verbose_name=_("Fecha de la premiación"),
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_premiado',
        verbose_name=_("Bombero premiado"),
    )
    premio_otorgado = models.CharField(
        max_length=500,
        verbose_name=_("Premio Otorgado"),
    )

    class Meta:
        verbose_name = _("Acta de Premio")
        verbose_name_plural = _("Actas de Premios")


class Pase(Acta):
    fecha_efectiva = models.DateField(
        default=timezone.now,
        verbose_name=_("Fecha efectiva del pase"),
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_solicitante',
        verbose_name=_("Bombero solicitante")
    )
    institucion_origen = models.ForeignKey(
        Institucion,
        related_name='institucion_origen',
        verbose_name=_("Institución Origen"),
    )
    institucion_destino = models.ForeignKey(
        Institucion,
        related_name='institucion_destino',
        verbose_name=_("Institución Destino")
    )

    class Meta:
        verbose_name = _("Acta de Pase")
        verbose_name_plural = _("Actas de Pases")
