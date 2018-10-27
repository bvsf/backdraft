from django.db import models
from datetime import date, datetime
from decimal import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _
from grados.models import Grado
from localidades.models import Localidad
from personas.models import Persona, Cuartelero, Institucion
from actas.models import Acta
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
    TIPO_SANCION,
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
        related_name="bomberos",
        on_delete=models.PROTECT,
    )
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
        verbose_name=_("Lugar de Nacimiento"),
        on_delete=models.PROTECT,
    )

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
            fecha_cuartel = self.bombero_ascendido.all()[0].acta.fecha_acta
        except IndexError:
            fecha_cuartel = self.bombero_solicitante.all()[0].acta.fecha_acta
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
        related_name="numeros_orden_bombero",
        on_delete=models.PROTECT,
    )
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


class Parentesco(models.Model):
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        related_name="bombero",
        on_delete=models.PROTECT,
    )
    familiar = models.ForeignKey(
        Persona,
        verbose_name=_("Familiar"),
        related_name="familiar",
        on_delete=models.PROTECT,
    )
    parentesco = models.CharField(
        max_length=255,
        choices=RELACION_PARENTESCO,
        default=RELACION_PARENTESCO[0][0],
        verbose_name=_("Parentesco"))


class Empleo(models.Model):
    empresa = models.ForeignKey(
        Institucion,
        verbose_name=_("Empresa"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        on_delete=models.PROTECT,
    )
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
        verbose_name=_("Establecimiento"),
        on_delete=models.PROTECT,
    )
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"),
        on_delete=models.PROTECT,
    )
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
        related_name="bombero_calificacion",
        on_delete=models.PROTECT,
    )
    periodo = models.IntegerField(
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Año"))
    puntaje_en_numero = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_("Puntaje Numérico"))

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

    def clean(self):
        if (self.puntaje_en_numero < 0) or (self.puntaje_en_numero > 20):
            raise ValidationError(_(
                'Puntaje Numérico fuera de los límites establecidos.'))

    def __str__(self):
        return "{0} {1} {2}".format(
            self.bombero,
            self.periodo,
            self.calificacion_escrita)

    class Meta:
        verbose_name = _("Calificación Anual")
        verbose_name_plural = _("Calificaciones Anuales")


class Licencia(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='acta_licencia',
        verbose_name=_("Acta"),
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
    bombero = models.ForeignKey(
        Bombero,
        related_name='bombero_licenciado',
        verbose_name=_("Bombero"),
        on_delete=models.PROTECT,
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


class ActaAscenso(models.Model):
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

    # TODO: obtener todos los ascensos del acta.


class Ascenso(models.Model):
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
        if ascenso and self.id is None:
            raise ValidationError(
                {'grado_ascenso':
                 _("Ya existe un ascenso para este bombero "
                   "para el mismo grado ({})".format(
                     ascenso.acta_ascenso.nombre_completo))}
            )


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


class Pase(models.Model):
    acta = models.ForeignKey(
        Acta,
        related_name='acta_pase',
        verbose_name=_("Acta"),
        on_delete=models.PROTECT,
    )
    fecha_efectiva = models.DateField(
        default=timezone.now,
        verbose_name=_("Fecha efectiva del pase"),
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
            self.acta.nombre_corto,
            self.bombero,
            self.institucion_origen,
            self.institucion_destino,
            self.fecha_efectiva,
        )
