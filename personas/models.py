# -*- coding: UTF-8 -*-
from datetime import date
from decimal import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext as _
from localidades.models import Localidad
from phonenumber_field.modelfields import PhoneNumberField
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
    GENERO,
)


class Entidad(models.Model):
    tipo_cuit = models.CharField(
        max_length=4,
        verbose_name=_("CUIT/CUIL"),
        choices=CUIT_CUIL,
        default=CUIT_CUIL[0][0])
    nro_cuit = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        verbose_name=_('Numero de CUIT/CUIL'))

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
        verbose_name=_("Razón Social"))

    def __str__(self):
        return self.razon_social

    @property
    def nombre_completo(self):
        return "({0}: {1}) - {0}".format(
            self.tipo_cuit,
            self.nro_cuit,
            self.razon_social)

    class Meta:
        verbose_name = _("Institución")
        verbose_name_plural = _("Instituciones")


class Persona(Entidad):
    apellido = models.CharField(
        max_length=255,
        verbose_name=_('Apellido'))
    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre'))
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
        blank=True)
    genero = models.CharField(
        max_length=255,
        choices=GENERO,
        default=GENERO[0][0],
        verbose_name=_("Genero"))

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
        return "{0} ({1})".format(
            self.nombre_completo,
            self.dni)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')

    def save(self, *args, **kwargs):
        usuario_id = None
        if hasattr(self, 'cuarteleros'):
            cuartelero = Cuartelero.objects.get(persona__id=self.pk)
            usuario_id = cuartelero.usuario.id
        elif hasattr(self, 'bomberos'):
            bombero = Bombero.objects.get(persona__id=self.pk)
            usuario_id = bombero.usuario.id

        if usuario_id:
            usuario = User.objects.get(pk=usuario_id)
            usuario.last_name = self.apellido
            usuario.first_name = self.nombre
            usuario.save()

        super(Persona, self).save(*args, **kwargs)


class Cuartelero(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="cuarteleros")
    persona = models.OneToOneField(
        Persona,
        verbose_name=_("Persona"),
        related_name="cuarteleros")

    def __str__(self):
        return self.persona.nombre_completo

    def sangre(self):
        return self.persona.sangre

    def dni(self):
        return self.persona.dni

    def fecha_nacimiento(self):
        return self.persona.fecha_nacimiento

    def save(self, *args, **kwargs):
        # No podemos crear un signal en el model User que viene con django,
        #   por ende hacemos esto acá
        # Como se crea el usuario únicamente cuando creamos el objeto no nos
        #   tenemos que preocupar que se modifique el usuario cuando se modifi-
        #   que el objeto. Para inhabilitar el usuario tendra que hacerlo el
        #   administrador.
        if not self.pk:
            dic = {
                'email': '',
                'password': self.persona.documento,
                'last_name': self.persona.apellido,
                'first_name': self.persona.nombre
            }

            # Si la persona es un bombero uso su mismo usuario
            # El primer parametro de update_or_create es lo que se usa para bus-
            #   -car si el registro existe, en defaults se pone los valores a
            #   rellenar si es que lo tiene que crear.
            try:
                bombero = Bombero.objects.get(persona__id=self.persona.pk)
                dic['username'] = bombero.usuario.username
                usuario_id = bombero.usuario.id
            except ObjectDoesNotExist:
                dic['username'] = self.persona.nombre.split()[0].lower() + \
                                 self.persona.apellido.lower()
                usuario_id = None
            self.usuario, created = User.objects.update_or_create(
                pk=usuario_id,
                defaults=dic
            )

            super(Cuartelero, self).save(*args, **kwargs)


class Bombero(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="bomberos")
    persona = models.OneToOneField(
        Persona,
        verbose_name=_("Persona"),
        related_name="bomberos")
    foto = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name=_("Foto Carnet"))
    numero_credencial = models.CharField(
        max_length=255,
        verbose_name=_("Número de Credencial"),
        unique=True)
    fecha_vencimiento = models.DateField(
        verbose_name=_('Fecha de Vencimiento'))
    estado_civil = models.CharField(
        max_length=255,
        choices=ESTADO_CIVIL,
        default=ESTADO_CIVIL[0][0],
        verbose_name=_("Estado Civil"))
    lugar_nacimiento = models.ForeignKey(
        Localidad,
        verbose_name=_("Lugar de Nacimiento"))

    def get_ultimo_ascenso(self):
        return self.bombero_ascendido.order_by(
            '-acta_ascenso__fecha_efectiva').first()

    # def get_orden_actual(self):
    #    return self.numero_orden_bombero.get_numero_orden_vigente()

    @property
    def get_grado_ultimo_ascenso(self):
        try:
            return self.get_ultimo_ascenso().grado_ascenso
        except AttributeError:
            return None

    @property
    def antiguedad_bombero(self):
        fecha_bombero = self.bombero_ascendido.get(
            grado_ascenso__nombre='Bombero').acta_ascenso.fecha_efectiva
        delta = (date.today() - fecha_bombero)
        return int(delta.days / 365.2425)

    def __str__(self):
        return "0{} - {}".format(
            self.numeros_orden_bombero.filter(vigencia_hasta__isnull=True).first().numero_orden,
            self.persona.nombre_completo,
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            dic = {
                'email': '',
                'password': self.persona.documento,
                'last_name': self.persona.apellido,
                'first_name': self.persona.nombre
            }

            # Si la persona es un bombero uso su mismo usuario
            # El primer parametro de update_or_create es lo que se usa para bus-
            #   -car si el registro existe, en defaults se pone los valores a
            #   rellenar si es que lo tiene que crear.
            try:
                cuartelero = Cuartelero.objects.get(persona__id=self.persona.pk)
                dic['username'] = cuartelero.usuario.username
                usuario_id = cuartelero.usuario.id
            except ObjectDoesNotExist:
                dic['username'] = self.persona.nombre.split()[0].lower() + \
                                 self.persona.apellido.lower()
                usuario_id = None
            self.usuario, created = User.objects.update_or_create(
                pk=usuario_id,
                defaults=dic
            )
        super(Bombero, self).save(*args, **kwargs)


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


class Medio(models.Model):
    entidad = models.ForeignKey(
        Entidad,
        related_name="entidad_%(class)s")
    uso = models.CharField(
        verbose_name=_("Uso"),
        max_length=255,
        choices=USO_MEDIO,
        default=USO_MEDIO[0][0])
    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Obervaciones"),
        blank=True,
        null=True)

    class Meta:
        abstract = True


class DireccionPostal(Medio):
    localidad = models.ForeignKey(
        Localidad,
        verbose_name=_("Localidad"),
        related_name="localidad")
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
            self.titulo)

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
        # https://docs.djangoproject.com/en/dev/
        #    ref/models/instances/#django.db.models.Model.get_FOO_display
        return "{0} - {1}".format(
            self.get_nivel_display(),
            self.get_estado_display())

    @property
    def estudio(self):
        return "({0})({1}) {2} - {3}".format(
            self.periodo,
            self.nivel_estudio,
            self.establecimiento,
            self.titulo)

    def __str__(self):
        return "{0}".format(
            self.estudio)


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
        if Decimal(19) <= self.puntaje_en_numero <= Decimal(20):
            return "{0}".format("Excelente")
        elif Decimal(15) <= self.puntaje_en_numero < Decimal(19):
            return "{0}".format("Muy Bueno")
        elif Decimal(10) <= self.puntaje_en_numero < Decimal(15):
            return "{0}".format("Bueno")
        elif Decimal(0) <= self.puntaje_en_numero < Decimal(10):
            return "{0}".format("Insuficiente")

    def __str__(self):
        return "{0} {1} {2}".format(
            self.bombero,
            self.periodo,
            self.calificacion_escrita)
