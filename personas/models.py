# -*- coding: UTF-8 -*-
from decimal import *
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext as _
from localidades.models import Localidad
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from .choices import (
    GRUPO_SANGUINEO,
    FACTOR_SANGUINEO,
    ESTADO_CIVIL,
    RELACION_PARENTESCO,
    USO_MEDIO,
    TIPO_WEB,
    TIPO_TELEFONO,
    TIPO_DOCUMENTO,
    CUIT_CUIL,
    NIVEL_ESTUDIO,
    ESTADO_ESTUDIO,
)


class Entidad(models.Model):
    tipo_cuit = models.CharField(
        max_length=4,
        verbose_name=_("CUIT/CUIL"),
        choices=CUIT_CUIL,
        default=CUIT_CUIL[0][0],
    )
    nro_cuit = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        verbose_name=_('Numero de CUIT/CUIL'),
    )

    def __str__(self):
        try:
            if hasattr(self, 'persona'):
                return "{0}".format(self.persona)
            elif hasattr(self, 'institucion'):
                return "{0}".format(self.institucion)
        except NotImplementedError:
            return _("ERROR! No es una Persona ni una Institución")


class Institucion(Entidad):
    razon_social = models.CharField(
        max_length=255,
        verbose_name=_("Razón Social"),
    )

    def __str__(self):
        return self.razon_social

    @property
    def nombre_completo(self):
        return "({0}: {1}) - {0}".format(
            self.tipo_cuit,
            self.nro_cuit,
            self.razon_social,
            )

    class Meta:
        verbose_name = _("Institución")
        verbose_name_plural = _("Instituciones")


class Persona(Entidad):
    apellido = models.CharField(
        max_length=255,
        verbose_name=_('Apellido')
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre')
    )
    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPO_DOCUMENTO,
        default=TIPO_DOCUMENTO[0][0],
        verbose_name=_("Tipo de Documento"))
    documento = models.CharField(
        max_length=11,
        verbose_name=_('Número de documento'),
        unique=True)
    grupo_sanguineo = models.CharField(
        max_length=255,
        choices=GRUPO_SANGUINEO,
        default=GRUPO_SANGUINEO[0][0],
        verbose_name=_("Grupo Sanguíneo"))
    factor_sanguineo = models.CharField(
        max_length=255,
        choices=FACTOR_SANGUINEO,
        default=FACTOR_SANGUINEO[0][0],
        verbose_name=_("Factor Sanguíneo"))
    fecha_nacimiento = models.DateField(
        verbose_name=_('Fecha de Nacimiento'))
    fecha_desceso = models.DateField(
        verbose_name=_("Fecha de Fallecimiento"),
        null=True,
        blank=True,)

    @property
    def nombre_completo(self):
        return "{0}, {1}".format(
            self.apellido.upper(),
            self.nombre)

    @property
    def edad(self):
        delta = (date.today() - self.fecha_nacimiento)
        return int(delta.days / 365.2425)

    @property
    def dni(self):
        return "{0} {1}".format(
            self.tipo_documento,
            self.documento)

    @property
    def sangre(self):
        return "{0} ({1})".format(
            self.grupo_sanguineo,
            self.factor_sanguineo)

    @property
    def aniversario(self):
        if self.fecha_desceso:
            delta = (date.today() - self.fecha_desceso)
            return int(delta.days / 365.2425)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')


class Bombero(models.Model):
    persona = models.OneToOneField(
        Persona,
        verbose_name=_("Persona"),
        related_name="bombero")
    foto = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name=_("Foto Carnet"))
    numero_credencial = models.CharField(
        max_length=255,
        verbose_name=_("Número de Credencial"),
        unique=True)
    estado_civil = models.CharField(
        max_length=255,
        choices=ESTADO_CIVIL,
        default=ESTADO_CIVIL[0][0],
        verbose_name=_("Estado Civil"))
    lugar_nacimiento = models.ForeignKey(
        Localidad,
        verbose_name=_("Lugar de Nacimiento"))

    def __str__(self):
        return self.persona.nombre_completo


class Parentesco(models.Model):
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        related_name="bombero")
    familiar = models.ForeignKey(
        Persona,
        verbose_name=_("Familiar"),
        related_name="familiar")
    parentesco = models.CharField(
        max_length=255,
        choices=RELACION_PARENTESCO,
        default=RELACION_PARENTESCO[0][0],
        verbose_name=_("Parentesco"))


class NumeroOrden(models.Model):
    numero_orden = models.SmallIntegerField(
        verbose_name=_("Número de Orden")
    )
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        related_name="numero_orden_bombero")
    vigencia_desde = models.DateField(
        default=timezone.now,
    )
    vigencia_hasta = models.DateField(
        null=True,
        blank=True,
    )

    @property
    def vigencia(self):
        vigencia = "vigente desde "
        if self.vigencia_hasta:
            vigencia += "{0} hasta el {1}".format(
                self.vigencia_desde,
                self.vigencia_hasta,
            )
        else:
            vigencia += "{0}".format(
                self.vigencia_desde,
            )
        return vigencia

    def cierre_vigencia(self):
        numero = NumeroOrden.objects.filter(
            bombero=self.bombero,
            vigencia_desde__lt=self.vigencia_desde,
            vigencia_hasta__isnull=True,
        )
        if numero:
            numero.update(vigencia_hasta=self.vigencia_desde)

    def clean(self):
        numero = NumeroOrden.objects.filter(
            bombero=self.bombero,
            vigencia_desde__gte=self.vigencia_desde,).count()
        if numero > 0 and self.id is None:
            raise ValidationError(
                {'vigencia_desde':
                 _("Ya existe un bombero con este número de orden vigente")})

    def save(self, *args, **kwargs):
        '''Siempre que se guarde un bombero se pone al final de la lista con el
        numero de orden mas bajo. Luego el sistema tendra que reordenarlo de
        acuerdo a los criterios que se decida.'''
        mayor = NumeroOrden.objects.filter(
            vigencia_hasta__isnull=True,
        ).order_by('-numero_orden')[:1]
        self.numero_orden = mayor + 1
        super(NumeroOrden, self).save(*args, **kwargs)

    def __str__(self):
        return "{0} - {1} ({2})".format(
            self.numero_orden,
            self.bombero,
            self.vigencia
        )


class Medio(models.Model):
    entidad = models.ForeignKey(Entidad)
    uso = models.CharField(
        verbose_name=_("Uso"),
        max_length=255,
        choices=USO_MEDIO,
        default=USO_MEDIO[0][0]
    )
    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Obervaciones"),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class DireccionPostal(Medio):
    localidad = models.ForeignKey(
        Localidad,
        verbose_name=_("Localidad"))
    calle = models.CharField(
        max_length=255,
        verbose_name=_("Calle"))
    numero = models.SmallIntegerField(
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


class DireccionWeb(Medio):
    direccion = models.URLField(
        verbose_name=_("Dirección Web"))
    tipo = models.CharField(
        max_length=255,
        choices=TIPO_WEB,
        default=TIPO_WEB[0][0],
        verbose_name=_("Tipo web"))

    def __str__(self):
        return self.direccion

    class Meta:
        verbose_name = _("Dirección Web")
        verbose_name_plural = _("Direcciones Web")


class Telefono(Medio):
    telefono = PhoneNumberField(
        verbose_name=_("Teléfono"))
    tipo = models.CharField(
        max_length=255,
        choices=TIPO_TELEFONO,
        default=TIPO_TELEFONO[0][0],
        verbose_name=_("Tipo de Teléfono"))

    def __str__(self):
        return self.telefono.__str__()

    class Meta:
        verbose_name = _("Teléfono")
        verbose_name_plural = _("Teléfonos")


class DireccionElectronica(Medio):
    mail = models.EmailField(
        verbose_name=_("Email"))

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = _("Direccion de Email")
        verbose_name_plural = _("Direcciones de Email")


class Empleo(models.Model):
    empresa = models.ForeignKey(
        Institucion,
        verbose_name=_("Empresa"))
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"))
    titulo = models.CharField(
        max_length=255,
        verbose_name=_("Título o cargo"))
    periodo_desde = models.DateField(
        verbose_name=_("Fecha de Inicio"))
    periodo_hasta = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Fecha de Fin"))
    descripcion = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_("Descripción"))

    class Meta:
        verbose_name = _("Empleo")
        verbose_name_plural = _("Empleos")

    @property
    def periodo(self):
        periodo = "Desde el {0} hasta".format(
            self.periodo_desde)
        if self.periodo_hasta:
            periodo += " el {0}".format(
                self.periodo_hasta)
        else:
            periodo += ' la actualidad'
        return "{0}".format(periodo)

    @property
    def trabajo(self):
        return "({0}) {1} - {2}".format(
            self.periodo,
            self.empresa,
            self.titulo,
            )

    def __str__(self):
        return "{0} - {1} ({2})".format(
            self.bombero,
            self.empresa,
            self.periodo)


class Estudio(models.Model):
    establecimiento = models.ForeignKey(
        Institucion,
        verbose_name=_("Establecimiento"))
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"))
    nivel = models.CharField(
        max_length=5,
        choices=NIVEL_ESTUDIO,
        default=NIVEL_ESTUDIO[0][0],
        verbose_name=_("Nivel de Estudio"))
    estado = models.CharField(
        max_length=5,
        choices=ESTADO_ESTUDIO,
        default=ESTADO_ESTUDIO[0][0],
        verbose_name=_("Estado de cursado"))
    titulo = models.CharField(
        max_length=255,
        verbose_name=_("Título"))
    periodo_desde = models.DateField(
        verbose_name=_("Fecha de Inicio"))
    periodo_hasta = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Fecha de Fin"))
    descripcion = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_("Descripción"))

    class Meta:
        verbose_name = _("Estudio")
        verbose_name_plural = _("Estudios")

    @property
    def periodo(self):
        periodo = "Desde el {0} hasta".format(
            self.periodo_desde)
        if self.periodo_hasta:
            periodo += " el {0}".format(
                self.periodo_hasta)
        else:
            periodo += ' la actualidad'
        return "{0}".format(periodo)

    @property
    def nivel_estudio(self):
        '''
        https://docs.djangoproject.com/en/dev/
            ref/models/instances/#django.db.models.Model.get_FOO_display
        '''
        return "{0} - {1}".format(
            self.get_nivel_display(),
            self.get_estado_display(),
            )

    @property
    def estudio(self):
        return "({0})({1}) {2} - {3}".format(
            self.periodo,
            self.nivel_estudio,
            self.establecimiento,
            self.titulo,
            )

    def __str__(self):
        return "{0}".format(
            self.estudio
            )


class CalificacionAnual(models.Model):

    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        related_name="bombero_calificacion")
    periodo = models.IntegerField(
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Año"))
    puntaje_en_numero = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_("Puntaje Numérico"))

    class Meta:
        verbose_name = _("Calificación Anual")
        verbose_name_plural = _("Calificaciones Anuales")

    def clean(self):
        if (self.puntaje_en_numero < 0) or (self.puntaje_en_numero > 20):
            raise ValidationError(_(
                'Puntaje Numérico fuera de los límites establecidos.'))

    @property
    def calificacion_escrita(self):
        if self.puntaje_en_numero >= Decimal(19) and \
        self.puntaje_en_numero <= Decimal(20):
            return "{0}".format(
                "Excelente"
            )
        elif self.puntaje_en_numero < Decimal(19) and \
        self.puntaje_en_numero >= Decimal(15):
            return "{0}".format(
                "Muy Bueno"
            )
        elif self.puntaje_en_numero < Decimal(15) and \
        self.puntaje_en_numero >= Decimal(10):
            return "{0}".format(
                "Bueno"
            )
        elif self.puntaje_en_numero < Decimal(10) and \
        self.puntaje_en_numero >= Decimal(0):
            return "{0}".format(
                "Insuficiente"
            )

    def __str__(self):
        return "{0} {1} {2}".format(
            self.bombero,
            self.periodo,
            self.calificacion_escrita)
