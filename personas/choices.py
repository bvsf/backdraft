# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

GRUPO_SANGUINEO = (
    ('', _('Grupo Saguineo')),
    ('AB', _('Grupo AB')),
    ('A', _('Grupo A')),
    ('B', _('Grupo B')),
    ('O', _('Grupo O')),
)

FACTOR_SANGUINEO = (
    ('', _('Factor Saguineo')),
    ('+', _('RH+')),
    ('-', _('RH-')),
)

ESTADO_CIVIL = (
    ('', _('Estado Civil')),
    ('Casado', _('Casado/a')),
    ('Soltero', _('Soltero/a')),
    ('Divorciado', _('Divorciado/a')),
    ('Viudo', _('Viudo/a')),
    ('Concubino', _('Concubino/a')),
)

RELACION_PARENTESCO = (
    ('', _('Relacion de Parentesco')),
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
    ('', _("Uso dado")),
    ('P', _("Particular")),
    ('L', _("Laboral")),
)

TIPO_WEB = (
    ('', _("Tipo de dirección web")),
    ('S', _("Perfil Web Social")),
    ('L', _("Pagina Web Laboral")),
)

TIPO_TELEFONO = (
    ('', _("Tipo de Teléfono")),
    ('C', _("Celular")),
    ('F', _("Fijo"))
)
