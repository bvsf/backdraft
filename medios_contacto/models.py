from django.db import models
from django.utils.translation import ugettext_lazy as _
from localidades.models import Localidad
from phonenumber_field.modelfields import PhoneNumberField
from .choices import USO_MEDIO, TIPO_WEB, TIPO_TELEFONO


class Medio(models.Model):
    uso = models.CharField(
        verbose_name=_("Uso"),
        max_length=255,
        choices=USO_MEDIO)
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
        verbose_name=_("Tipo de Teléfono"))

    def __str__(self):
        return self.telefono

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