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
            self.razon_social)

    class Meta:
        verbose_name = _("Institución")
        verbose_name_plural = _("Instituciones")


class Persona(Entidad):
    apellido = models.CharField(
        max_length=255,
        verbose_name=_('Apellido'),
    )
    primer_nombre = models.CharField(
        max_length=255,
        verbose_name=_('Primer Nombre'),
    )
    segundo_nombre = models.CharField(
        max_length=255,
        verbose_name=_('Segundo Nombre'),
        null=True,
        blank=True,
    )
    tercer_nombre = models.CharField(
        max_length=255,
        verbose_name=_('Tercer Nombre'),
        null=True,
        blank=True,
    )
    # Algunos registros históricos no tienen el tipo de documento,
    #   le ponemos a todos DNI
    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPO_DOCUMENTO,
        default=TIPO_DOCUMENTO[0][0],
        verbose_name=_("Tipo de Documento"),
    )
    # Algunos registros históricos, y otros actuales no está el DNI
    #   pero no podemos sacarle el unique True, hay que corregir el archivo de migracion
    documento = models.CharField(
        max_length=11,
        verbose_name=_('Número de documento'),
        unique=True,
    )
    # No está el grupo sanguíneo de los registros históricos
    grupo_sanguineo = models.CharField(
        max_length=255,
        choices=GRUPO_SANGUINEO,
        default=GRUPO_SANGUINEO[0][0],
        verbose_name=_("Grupo Sanguíneo"),
        null=True,
        blank=True,
    )
    # Al igual que el grupo sanguíneo, el factor tampoco está en los históricos
    factor_sanguineo = models.CharField(
        max_length=255,
        choices=FACTOR_SANGUINEO,
        default=FACTOR_SANGUINEO[0][0],
        verbose_name=_("Factor Sanguíneo"),
        null=True,
        blank=True,
    )
    # Algunos registros históricos con tienen la fecha de nacimiento indicada
    fecha_nacimiento = models.DateField(
        verbose_name=_('Fecha de Nacimiento'),
        null=True,
        blank=True,
    )
    fecha_desceso = models.DateField(
        verbose_name=_("Fecha de Fallecimiento"),
        null=True,
        blank=True,
    )
    genero = models.CharField(
        max_length=255,
        choices=GENERO,
        default=GENERO[0][0],
        verbose_name=_("Genero"),
    )

    @property
    def nombre_completo(self):
        nombre = "{0}, {1}".format(
            self.apellido.upper(),
            self.primer_nombre.capitalize()
        )
        if self.segundo_nombre:
            nombre += " {0}".format(self.segundo_nombre.capitalize())
        if self.tercer_nombre:
            nombre += " {0}".format(self.tercer_nombre.capitalize())
        return nombre

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
        ordering = ['apellido', 'primer_nombre']
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
    '''
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
            usuario.first_name = self.primer_nombre
            usuario.save()

        super(Persona, self).save(*args, **kwargs)
    '''


class Cuartelero(models.Model):
    usuario = models.OneToOneField(
        User,
        related_name="cuarteleros",
        on_delete=models.PROTECT,
    )
    persona = models.OneToOneField(
        Persona,
        verbose_name=_("Persona"),
        related_name="cuarteleros",
        on_delete=models.PROTECT,
    )

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
                'last_name': self.persona.apellido,
                'first_name': self.persona.primer_nombre,
                'username': self.persona.primer_nombre.split()[0].lower() + self.persona.apellido.lower()
            }
            # Si la persona es un bombero uso su mismo usuario
            # El primer parametro de update_or_create es lo que se usa para bus-
            #   -car si el registro existe, en defaults se pone los valores a
            #   rellenar si es que lo tiene que crear.
            try:
                usuario = User.objects.get(username=dic['username'])
                usuario_id = usuario.pk
            except ObjectDoesNotExist:
                usuario_id = None
            self.usuario, created = User.objects.update_or_create(
                pk=usuario_id,
                defaults=dic
            )
            if created:
                self.usuario.set_password(self.persona.documento)
                self.usuario.save()

            super(Cuartelero, self).save(*args, **kwargs)


class Medio(models.Model):
    entidad = models.ForeignKey(
        Entidad,
        related_name="entidad_%(class)s",
        on_delete=models.PROTECT,
    )
    uso = models.CharField(
        verbose_name=_("Uso"),
        max_length=255,
        choices=USO_MEDIO,
        default=USO_MEDIO[0][0])
    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Obervaciones"),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class DireccionPostal(Medio):
    localidad = models.ForeignKey(
        Localidad,
        verbose_name=_("Localidad"),
        related_name="localidad",
        on_delete=models.PROTECT,
    )
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
        return '{0} {1} {2} {3}'.format(
            self.calle,
            self.numero,
            self.piso,
            self.departamento,
        )

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
