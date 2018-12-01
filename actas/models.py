# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from bomberos.models import Bombero
from grados.models import Grado
from localidades.models import Localidad
from personas.models import Persona, Cuartelero, Institucion
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
        blank=True,
        null=True,
        max_length=1000)

    @property
    def nombre_completo(self):
        return _("Libro: {0} Folio: {1} Acta: {2} - Fecha: {3}").format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
            self.fecha_acta,
        )

    @property
    def nombre_corto(self):
        return _("{0}.{1}.{2} ({3})").format(
            self.numero_libro,
            self.numero_folio,
            self.numero_acta,
            self.fecha_acta,
        )

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

    def __str__(self):
        return "{0}".format(self.nombre_corto)


class ActaAscenso(models.Model):
    '''
    Las Incorporacines de Civiles a Bomberos se cargan como un ascenso  pero el rango deberá ser a Aspirante
        Mayor o Menor según corresponda su edad si es mayor o menor de 18 años.
    '''
    acta = models.ForeignKey(
        Acta,
        related_name='acta_ascenso',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    fecha_efectiva = models.DateField(
        verbose_name=_("Fecha efectiva de Ascenso"),
    )

    class Meta:
        verbose_name = _("Ascenso")
        verbose_name_plural = _("Ascensos")


class ActaLicencia(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='acta_licencia',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    fecha_efectiva = models.DateField(
        verbose_name=_("Fecha efectiva de Licencia"),
    )

    class Meta:
        verbose_name = _("Licencia")
        verbose_name_plural = _("Licencias")


class ActaPase(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='acta_pase',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    fecha_efectiva = models.DateField(
        verbose_name=_("Fecha efectiva de Pase"),
    )

    class Meta:
        verbose_name = _("Pase")
        verbose_name_plural = _("Pases")


class ActaSancion(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='actasancion',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    fecha_incidente = models.DateField(
        verbose_name=_("Fecha del Incidente"),
    )
    descripcion_incidente = models.CharField(
        max_length=500,
        verbose_name=_("Descripción del Incidente"),
    )

    def get_sanciones(self):
        return Sancion.objects.filter(actasancion=self)

    class Meta:
        verbose_name = _("Sanción")
        verbose_name_plural = _("Sanciones")


class Ascenso(models.Model):
    '''
    Si el bombero es un Civil, aún no debería tener asignado ningun Ascenso, en cuyo caso el grado de ascenso no puede
        ser otro que el de Aspirante Mayor o Menor segun tenga 18 o más años o menos de 18 años respectivamente.
    Si el bombero no es un civil, el grado de ascenso no puede ser igual al que ya tiene (o si ya tuvo un grado igual)
        en cuyo caso, también, el grado al que es ascendido debe ser mayor al actual.
    '''
    acta_ascenso = models.ForeignKey(
        ActaAscenso,
        related_name='ascenso',
        verbose_name=_("Acta Ascenso"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_ascendido',
        verbose_name=_("Bombero Ascendido"),
        on_delete=models.PROTECT,
    )
    grado_ascenso = models.ForeignKey(
        Grado,
        related_name='grado_ascendido',
        verbose_name=_("Grado Ascendido"),
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ['acta_ascenso']

    def __str__(self):
        return _("{0} ascendido a {1} el {2}").format(
            self.bombero,
            self.grado_ascenso,
            self.acta_ascenso.fecha_efectiva,
        )

    def clean(self):
        ascenso = Ascenso.objects.filter(
            bombero=self.bombero,
            grado_ascenso=self.grado_ascenso).first()
        # TODO: validar que el bombero no esté dado de baja.
        # TODO: validar que el bombero esté activo.
        # TODO: validar que el bombero si es civil el grado sea Aspirante mayor o menor segun su edad.
        if ascenso and self.id is None:
            raise ValidationError(
                {'grado_ascenso':
                    _("Ya existe un ascenso para este bombero "
                      "para el mismo grado ({})".format(
                        ascenso.acta_ascenso.nombre_completo))}
            )


class Licencia(models.Model):
    acta_licencia = models.ForeignKey(
        ActaLicencia,
        related_name='licencia',
        verbose_name=_("Licencia"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_licenciado',
        verbose_name=_("Bombero"),
        on_delete=models.PROTECT,
    )
    fecha_desde = models.DateField(
        verbose_name=_("Fecha desde"),
    )
    fecha_hasta = models.DateField(
        verbose_name=_("Fecha hasta"),
    )
    motivo = models.CharField(
        max_length=500,
        verbose_name=_("Motivo de la Licencia"),
    )

    @property
    def periodo_licencia(self):
        return _("Desde: {0} hasta: {1}").format(
            self.fecha_desde,
            self.fecha_hasta,
        )

    class Meta:
        verbose_name = _("Licencia")
        verbose_name_plural = _("Licencias")

    def __str__(self):
        return _("({0}) - Licencia desde {1} hasta {2}").format(
            self.acta.nombre_corto,
            self.fecha_desde,
            self.fecha_hasta,
        )


class Pase(models.Model):
    acta = models.ForeignKey(
        ActaPase,
        related_name='pase',
        verbose_name=_("Pase"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_solicitante',
        verbose_name=_("Bombero solicitante"),
        on_delete = models.PROTECT,
    )
    grado_origen = models.ForeignKey(
        Grado,
        related_name='grado_solicitante',
        verbose_name=_("Grado del solicitante"),
        on_delete=models.PROTECT,
    )
    fecha_ult_ascenso = models.DateField(
        verbose_name=_("Fecha último ascenso")
    )
    fecha_bombero = models.DateField(
        verbose_name=_("Fecha ascenso a Bombero"),
        blank=True,
        null=True,
    )
    grado_final = models.ForeignKey(
        Grado,
        related_name='grado_tomado_solicitante',
        verbose_name=_("Grado asignado al solicitante"),
        on_delete=models.PROTECT,
    )
    institucion_origen = models.ForeignKey(
        Institucion,
        related_name='institucion_origen',
        verbose_name=_("Institución Origen"),
        on_delete=models.PROTECT,
    )
    institucion_destino = models.ForeignKey(
        Institucion,
        related_name='institucion_destino',
        verbose_name=_("Institución Destino"),
        on_delete = models.PROTECT,
    )

    class Meta:
        verbose_name = _("Pase")
        verbose_name_plural = _("Pases")

    def __str__(self):
        return _("{0}: {1} pasó de {2} a {3} desde el {4}").format(
            self.actapase.acta.nombre_corto,
            self.bombero,
            self.institucion_origen,
            self.institucion_destino,
            self.actapase.fecha_efectiva,
        )


class Premio(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='acta_premio',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    fecha_premiacion = models.DateField(
        verbose_name=_("Fecha de la premiación"),
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_premiado',
        verbose_name=_("Bombero premiado"),
        on_delete=models.PROTECT,
    )
    premio_otorgado = models.CharField(
        max_length=500,
        verbose_name=_("Premio Otorgado"),
    )

    class Meta:
        verbose_name = _("Premio")
        verbose_name_plural = _("Premios")

    def __str__(self):
        return _("{0}: {1} premiado el {2} con {3}").format(
            self.acta.nombre_corto,
            self.bombero,
            self.fecha_premiacion,
            self.premio_otorgado,
        )


class Reincorporacion(models.Model):
    pass


class Renuncia(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='acta_renuncia',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_baja',
        verbose_name=_("Bombero dado de baja"),
        on_delete=models.PROTECT,
    )
    fecha_solicitud = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Fecha de solicitud de baja"),
    )
    fecha_efectiva = models.DateField(
        default=timezone.now,
        verbose_name=_("Fecha efectiva de baja"),
    )

    class Meta:
        verbose_name = _("Renuncia")
        verbose_name_plural = _("Renuncia")

    def __str__(self):
        return _("{0} dado de baja el {1}").format(
            self.bombero,
            self.fecha_efectiva,
        )

    def save(self, *args, **kwargs):
        # Cerrar vigencia del número de orden del bombero
        numero_orden = NumeroOrden.objects.filter(bombero=self.bombero).last()
        numero_orden.cerrar_vigencia()
        super(Renuncia, self).save(*args, **kwargs)


class Sancion(models.Model):
    acta_sancion = models.ForeignKey(
        ActaSancion,
        related_name='acta_sancion',
        verbose_name=_("Acta de Sanción"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_interviniente',
        verbose_name=_("Bombero interviniente"),
        on_delete=models.PROTECT,
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

    class Meta:
        ordering = ['acta_sancion']

    def __str__(self):
        linea = "{0} {1} {2}".format(
            self.acta_sancion.acta.nombre_corto,
            self.bombero,
            self.tipo_sancion)

        if self.dias_suspencion > 0:
            linea += _("Suspendido {0} días").format(self.dias_suspencion)

        return linea
