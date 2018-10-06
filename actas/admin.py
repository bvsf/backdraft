from django.contrib import admin
from django.utils.translation import ugettext as _
from actas.models import (
    Acta,

)


@admin.register(Acta)
class ActaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_libro',
                'numero_folio',
                'numero_acta',
                'fecha_acta',
                'descripcion_acta',
                )
        }),
    )


