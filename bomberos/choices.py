# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _


TIPO_SANCION = (
    ('advertencia', _("Advertencia")),
    ('suspencion', _("Suspención")),
    ('baja', _("Baja")),
    ('exoneracion', _("Exoneración")),
)

GENERO = (
    ('M', _('Masculino')),
    ('F', _('Femenino')),
)

GRUPO_SANGUINEO = (
    ('AB', _('Grupo AB')),
    ('A', _('Grupo A')),
    ('B', _('Grupo B')),
    ('O', _('Grupo O')),
)

FACTOR_SANGUINEO = (
    ('+', _('RH+')),
    ('-', _('RH-')),
)

ESTADO_CIVIL = (
    ('Casado', _('Casado/a')),
    ('Concubino', _('Concubino/a')),
    ('Divorciado', _('Divorciado/a')),
    ('Separado', _('Separado/a')),
    ('Soltero', _('Soltero/a')),
    ('Viudo', _('Viudo/a')),
)

RELACION_PARENTESCO = (
    ('Hermano', _('Hermano/a')),
    ('Padre', _('Padre')),
    ('Madre', _('Madre')),
    ('Hijo', _('Hijo/a')),
    ('Abuelo', _('Abuelo/a')),
    ('Nieto', _('Nieto/a')),
    ('Tio', _('Tío/a')),
    ('Primo', _('Primo/a')),
    ('Esposo', _('Esposo/a')),
)

USO_MEDIO = (
    ('P', _("Particular")),
    ('L', _("Laboral")),
)

TIPO_WEB = (
    ('S', _("Perfil Web Social")),
    ('L', _("Pagina Web Laboral")),
)

TIPO_TELEFONO = (
    ('C', _("Celular")),
    ('F', _("Fijo"))
)

TIPO_DOCUMENTO = (
    ('DNI', _("DNI")),
    ('LC', _("LC")),
    ('LE', _("LE")),
)

CUIT_CUIL = (
    ('CUIT', _("CUIT")),
    ('CUIL', _("CUIL")),
    )

ESTADO_ESTUDIO = (
    ('F', _("Finalizado")),
    ('C', _("Cursando")),
    ('A', _("Abandonado")),
    )

NIVEL_ESTUDIO = (
    ('P', _("Primario")),
    ('S', _("Secundario")),
    ('T', _("Terciario")),
    ('U', _("Universitario")),
    )