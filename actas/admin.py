from django.contrib import admin
from django.utils.translation import ugettext as _
from actas.models import (
    Licencia,
)


@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_libro',
                'numero_folio',
                'numero_acta',
                'fecha_acta',
                'descripcion_acta',
                'fecha_desde',
                'fecha_hasta',
                'bombero',
                )
        }),
    )
    list_display = (
            'acta',
            'fecha_acta',
            'periodo_licencia',
            'bombero',
    )
    list_filter = (
            'fecha_acta',
            'fecha_desde',
            'fecha_hasta',
            'bombero',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
            'fecha_desde',
            'fecha_hasta',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')

    def periodo_licencia(self, obj):
        return obj.periodo_licencia
    periodo_licencia.short_description = _('Licencia')
