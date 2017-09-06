from django.contrib import admin
from django.utils.translation import ugettext as _
from actas.models import (
    Licencia,
    ActaAscenso,
    Ascenso,
    ActaSancion,
    Sancion,
    Premio,
    Pase,
)


@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_libro',
                'numero_folio',
                'numero_acta',
                'fecha_acta',
                'descripcion_acta',
                'fecha_premiacion',
                'premio_otorgado',
                'bombero',
                )
        }),
    )
    list_display = (
            'acta',
            'fecha_acta',
            'fecha_premiacion',
            'premio_otorgado',
            'bombero',
    )
    list_filter = (
            'fecha_acta',
            'fecha_premiacion',
            'premio_otorgado',
            'bombero',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
            'fecha_premiacion',
            'premio_otorgado',
            'bombero',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')


@admin.register(Pase)
class PaseAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_libro',
                'numero_folio',
                'numero_acta',
                'fecha_acta',
                'descripcion_acta',
                'fecha_efectiva',
                'institucion_origen',
                'institucion_destino',
                'bombero',
                )
        }),
    )
    list_display = (
            'acta',
            'fecha_acta',
            'fecha_efectiva',
            'institucion_origen',
            'institucion_destino',
            'bombero',
    )
    list_filter = (
            'fecha_acta',
            'fecha_efectiva',
            'institucion_origen',
            'institucion_destino',
            'bombero',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
            'fecha_efectiva',
            'institucion_origen',
            'institucion_destino',
            'bombero',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')


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


class AscensoTabular(admin.TabularInline):
    model = Ascenso


@admin.register(ActaAscenso)
class ActaAscensoAdmin(admin.ModelAdmin):
    inlines = [
        AscensoTabular,
    ]
    list_display = (
            'acta',
            'fecha_acta',
            'fecha_efectiva',
    )
    list_filter = (
            'fecha_acta',
            'fecha_efectiva',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
            'fecha_efectiva',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')


class SancionTabular(admin.TabularInline):
    model = Sancion


@admin.register(ActaSancion)
class ActaSancionAdmin(admin.ModelAdmin):
    inlines = [
        SancionTabular,
    ]
    list_display = (
            'acta',
            'fecha_acta',
            'fecha_incidente',
    )
    list_filter = (
            'fecha_acta',
            'fecha_incidente',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
            'fecha_incidente',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')
