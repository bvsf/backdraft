# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from personas.models import Bombero, Institucion, Entidad, Persona


class Alergenos(models.Model):
    nombre_alergeno = models.CharField(
        max_length=255,
        verbose_name=_('Nombre del Alérgeno'))

    def __str__(self):
        return "{0}".format(
            self.nombre_alergeno)

    class Meta:
        verbose_name = _("Alérgeno")
        verbose_name_plural = _("Alérgenos")


class Alergicos(models.Model):
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"))
    alergeno = models.ForeignKey(
        Alergenos,
        verbose_name=_("Alérgeno"))

    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Observaciones"),
        blank=True,
        null=True)

    def __str__(self):
        return "{0} -> {1}".format(
            self.bombero,
            self.alergeno)

    class Meta:
        verbose_name = _("Alérgico")
        verbose_name_plural = _("Alérgicos")
        unique_together = (("bombero", "alergeno"),)


class ObraSocial(models.Model):
    institucion = models.OneToOneField(
        Institucion,
        verbose_name=_("Institución"))

    def __str__(self):
        return "{0}".format(
            self.institucion)

    class Meta:
        verbose_name = _("Obra Social")
        verbose_name_plural = _("Obras Sociales")


class PlanMedico(models.Model):
    descripcion = models.TextField(
        max_length=255,
        verbose_name=_('Descripción'))

    obraSocial = models.ForeignKey(
        ObraSocial,
        verbose_name=_("Obra Social"),
        related_name="obraSocial")

    def __str__(self):
        return "{0} ({1})".format(
            self.descripcion,
            self.obraSocial)

    class Meta:
        verbose_name = _("Plan Médico")
        verbose_name_plural = _("Planes Médicos")


class Clinica(models.Model):
    # TODO: Ver qué se le puede agregar a esta clase
    institucion = models.OneToOneField(
        Institucion,
        verbose_name=_("Institución"))

    def __str__(self):
        return "{0}".format(
            self.institucion,
        )

    class Meta:
        verbose_name = _("Clínica")
        verbose_name_plural = _("Clínicas")


class MedicoCabecera(models.Model):
    apellido = models.CharField(
        max_length=255,
        verbose_name=_('Apellido'))
    nombre = models.CharField(
        max_length=255,
        verbose_name=_('Nombre'))
    especialidad = models.CharField(
        max_length=255,
        verbose_name=_('Especialidad'))
    nroMatricula = models.CharField(
        max_length=11,
        verbose_name=_("Número de Matrícula"),
        unique=True)

    def __str__(self):
        return "{0}, {1} - {2} - Mat.:{3}".format(
            self.apellido,
            self.nombre,
            self.especialidad,
            self.nroMatricula)

    class Meta:
        verbose_name = _("Médico de Cabecera")
        verbose_name_plural = _("Médicos de Cabecera")
        unique_together = (("nombre", "apellido", "nroMatricula"),)


class CoberturaMedica(models.Model):
    planMedico = models.ForeignKey(
        PlanMedico,
        verbose_name=_("Plan Médico"))
    medicoCabecera = models.ForeignKey(
        MedicoCabecera,
        verbose_name=_("Médico de Cabecera"))
    clinica = models.ForeignKey(
        Clinica,
        verbose_name=_("Clínica"))
    bombero = models.ForeignKey(
        Bombero,
        verbose_name=_("Bombero"))
    nroAfiliado = models.CharField(
        max_length=11,
        verbose_name=_('Número de Afiliado'),
        unique=True)
    fechaInicio = models.DateField(
        verbose_name=_("Fecha de Inicio de Cobertura"),
        null=True
    )
    fechaFin = models.DateField(
        verbose_name=_("Fecha de Finalización de Cobertura"),
        blank=True,
        null=True)
    observaciones = models.TextField(
        max_length=1000,
        verbose_name=_("Observaciones"),
        blank=True,
        null=True)

    def __str__(self):
        return "Bombero:{0}, Nº Afiliado:{1}, Plan:{2}, Médico de cabecera:{3}, Clinica:{4}".format(
            self.bombero,
            self.nroAfiliado,
            self.planMedico,
            self.medicoCabecera,
            self.clinica)

    class Meta:
        verbose_name = _("Cobertura Médica")
        verbose_name_plural = _("Coberturas Médicas")
        unique_together = (("bombero", "planMedico"),)
