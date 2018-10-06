from django.db import models
from datetime import date
from decimal import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext as _
from localidades.models import Localidad
from personas.models import Persona, Cuartelero, Institucion
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


class Bombero(models.Model):
    """
        El numero de legajo del bombero es el PK pero Django no lo permite editar. OJO
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
        unique=True)
    fecha_vencimiento = models.DateField(
        verbose_name=_('Fecha de Vencimiento'),
        blank=True,
        null=True,)
    estado_civil = models.CharField(
        max_length=255,
        choices=ESTADO_CIVIL,
        default=ESTADO_CIVIL[0][0],
        null=True,
        blank=True,
        verbose_name=_("Estado Civil"))
    lugar_nacimiento = models.ForeignKey(
        Localidad,
        null=True,
        blank=True,
        verbose_name=_("Lugar de Nacimiento"))

    def get_ultimo_ascenso(self):
        return self.bombero_ascendido.order_by(
            '-acta_ascenso__fecha_efectiva').first()

    @property
    def get_grado_ultimo_ascenso(self):
        try:
            return self.get_ultimo_ascenso().grado_ascenso
        except AttributeError:
            return self.bombero_solicitante.get().grado_final

    @property
    def antiguedad_bombero(self):
        # TODO: Así como está si tiene una reincorporación con el grado BV te trae esa fecha y en realidad puede ser
        #   anterior. Hay que tomar la más vieja o bien crear un campo.
        try:
            fecha_bombero = self.bombero_ascendido.get(
                grado_ascenso__nombre='Bombero').acta_ascenso.fecha_efectiva
        except ObjectDoesNotExist:
            fecha_bombero = self.bombero_solicitante.get().fecha_bombero
        if fecha_bombero:
            delta = (date.today() - fecha_bombero)
            return int(delta.days / 365.2425)
        else:
            return None

    @property
    def antiguedad_cuartel(self):
        # TODO: Acá falta hacer el cálculo del tiempo que pudo haber estado dado de baja y de sus reincorporaciones
        try:
            fecha_cuartel = self.bombero_ascendido.all()[0].fecha_acta
        except:
            fecha_cuartel = self.bombero_solicitante.all()[0].fecha_acta
        if fecha_cuartel:
            delta = (date.today() - fecha_cuartel)
            return int(delta.days / 365.2425)
        else:
            return None

    def __str__(self):
        try:
            return "0{} - {}".format(
                self.numeros_orden_bombero.filter(vigencia_hasta__isnull=True).first().numero_orden,
                self.persona.nombre_completo,
            )
        except AttributeError:
            return "{}".format(
                self.persona.nombre_completo,
            )

    def save(self, *args, **kwargs):
        if not self.pk:
            dic = {
               'email': '',
               'last_name': self.persona.apellido,
               'first_name': self.persona.primer_nombre
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
                dic['username'] = self.persona.primer_nombre.split()[0].lower() + \
                                 self.persona.apellido.lower()
                usuario_id = None
            self.usuario, created = User.objects.update_or_create(
                pk=usuario_id,
                defaults=dic
            )
            if created:
                self.usuario.set_password(self.persona.documento)
                self.usuario.save()

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
