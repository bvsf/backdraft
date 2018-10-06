from django.contrib import admin
from django.utils.translation import ugettext as _
from actas.models import (
    Acta,
    Licencia,
    ActaAscenso,
    Ascenso,
    Renuncia,
    ActaSancion,
    Sancion,
    Premio,
    Pase,
)


@admin.register(Acta)
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
                )
        }),
    )


@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'acta',
                'fecha_premiacion',
                'premio_otorgado',
                'bombero',
                )
        }),
    )
    '''
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
    '''


@admin.register(Pase)
class PaseAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'acta',
                'fecha_efectiva',
                'institucion_origen',
                'institucion_destino',
                'bombero',
                'grado_origen',
                'grado_final',
                'fecha_ult_ascenso',
                'fecha_bombero'
                )
        }),
    )
    '''
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
    '''


@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'acta',
                'fecha_desde',
                'fecha_hasta',
                'bombero',
                )
        }),
    )
    '''
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
    '''


@admin.register(Renuncia)
class RenunciaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'acta',
                'bombero',
                'fecha_solicitud',
                'fecha_efectiva',
            )
        }),
    )
    '''
    list_display = (
        'bombero',
        'fecha_solicitud',
        'fecha_efectiva',
    )
    list_filter = (
        'bombero',
        'fecha_solicitud',
        'fecha_efectiva',
    )
    search_fields = (
        'bombero',
        'fecha_solicitud',
        'fecha_efectiva',
        'numero_libro',
        'numero_folio',
        'numero_acta',
        'fecha_acta',
        'descripcion_acta',
        'fecha_desde',
        'fecha_hasta',
    )
    '''


class AscensoTabular(admin.TabularInline):
    model = Ascenso


@admin.register(ActaAscenso)
class ActaAscensoAdmin(admin.ModelAdmin):
    inlines = [
        AscensoTabular,
    ]
    '''
    list_display = (
            'acta__nombre_corto',
            'acta__fecha_acta',
            'fecha_efectiva',
    )
    list_filter = (
            'acta__fecha_acta',
            'fecha_efectiva',
    )
    search_fields = (
            'acta__numero_libro',
            'acta__numero_folio',
            'acta__numero_acta',
            'acta__fecha_acta',
            'acta__descripcion_acta',
            'fecha_efectiva',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')
    '''


class SancionTabular(admin.TabularInline):
    model = Sancion


@admin.register(ActaSancion)
class ActaSancionAdmin(admin.ModelAdmin):
    inlines = [
        SancionTabular,
    ]
    '''
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
    '''
