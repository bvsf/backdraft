from django.contrib import admin
from django.utils.translation import ugettext as _
from personas.models import (
    Persona,
    Bombero,
    DireccionPostal,
    DireccionWeb,
    Telefono,
    DireccionElectronica,
    Parentesco,
    Estudio,
    Empleo,
    Institucion,
    CalificacionAnual,
    NumeroOrden,
)


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo_cuit',
                'nro_cuit',
                'razon_social',
                )
        }),
    )
    list_display = (
        'tipo_cuit',
        'nro_cuit',
        'razon_social',
    )
    search_fields = (
        'nro_cuit',
        'razon_social',
    )


@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'establecimiento',
                'nivel',
                'titulo',
                'estado',
                'periodo_desde',
                'periodo_hasta',
                )
        }),
        (_('Descripcion'), {
            'classes': ('collapse',),
            'fields': ('descripcion',),
        }),
    )
    list_display = (
        'periodo',
        'establecimiento',
        'bombero',
    )
    search_fields = (
        'bombero__persona__apellido',
        'bombero__persona__nombre',
        'bombero__persona__documento',
        'bombero__persona__nro_cuit',
        'establecimiento__razon_social',
        'establecimiento__nro_cuit',
        'nivel',
        'estado',
        'titulo',
    )
    list_filter = (
        'bombero',
        'establecimiento',
        'nivel',
        'estado',
        'titulo',
    )
    date_hierarchy = 'periodo_desde'

    def periodo(self, obj):
        return obj.periodo
    periodo.short_description = _('Periodo')


@admin.register(Empleo)
class EmpleoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'empresa',
                'titulo',
                'periodo_desde',
                'periodo_hasta',
                )
        }),
        (_('Descripcion'), {
            'classes': ('collapse',),
            'fields': ('descripcion',),
        }),
    )
    list_display = (
        'periodo',
        'empresa',
        'bombero',
    )
    search_fields = (
        'bombero__persona__apellido',
        'bombero__persona__nombre',
        'bombero__persona__documento',
        'bombero__persona__nro_cuit',
        'empresa__razon_social',
        'empresa__nro_cuit',
        'titulo',
    )
    list_filter = (
        'bombero',
        'empresa',
    )
    date_hierarchy = 'periodo_desde'

    def periodo(self, obj):
        return obj.periodo
    periodo.short_description = _('Periodo')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo_cuit',
                'nro_cuit',
                'apellido',
                'nombre',
                'tipo_documento',
                'documento',
                'grupo_sanguineo',
                'factor_sanguineo',
                'fecha_nacimiento',)
        }),
        (_('¿Fallecido?'), {
            'classes': ('collapse',),
            'fields': ('fecha_desceso',),
        }),
    )
    list_display = (
        'nombre_completo',
        'dni',
        'sangre',
        'fecha_nacimiento',
        'fecha_desceso',)
    search_fields = (
        'apellido',
        'nombre',
        'documento',
        'nro_cuit',
    )
    list_filter = (
        'apellido',
        'fecha_nacimiento',
        'tipo_documento',
        'grupo_sanguineo',
        'factor_sanguineo',
        'fecha_desceso',)
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Bombero)
class BomberoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'persona',
                'numero_credencial',
                'fecha_vencimiento',
                'foto',
                'estado_civil',
                'lugar_nacimiento',
                )
        }),
    )
    list_display = (
        'numero_credencial',
        'fecha_vencimiento',
        'nombre_completo',
        'dni',
        'sangre',
    )

    def nombre_completo(self, obj):
        return obj.persona.nombre_completo
    nombre_completo.short_description = _('Apellido y Nombre')

    def sangre(self, obj):
        return obj.persona.sangre
    sangre.short_description = _('Grupo Sanguíneo')

    def dni(self, obj):
        return obj.persona.dni
    dni.short_description = _('Documento')

    search_fields = (
        'persona__apellido',
        'persona__nombre',
        'persona__documento',
        'persona__nro_cuit',
    )


@admin.register(Parentesco)
class ParentescoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'bombero',
        'familiar',
        'parentesco',)
    search_fields = (
        'bombero.persona.apellido',
        'bombero.persona.nombre',
        'familiar.apellido',
        'familiar.nombre',)


@admin.register(DireccionPostal)
class DireccionPostalAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'uso',
                'calle',
                'numero',
                'piso',
                'departamento',
                'localidad')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    search_fields = (
        'calle',
        'numero',
        'piso',
        'departamento',
        'localidad__nombre')
    list_display = (
        'entidad',
        'direccion_completa',
    )
    list_filter = (
        'entidad',
        'uso',
        'localidad')


@admin.register(DireccionWeb)
class DireccionWebAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'tipo',
                'uso',
                'direccion')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    list_display = (
        'entidad',
        'tipo',
        'uso',
        'direccion')
    list_filter = (
        'entidad',
        'tipo',
        'uso')


@admin.register(Telefono)
class TelefonoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'tipo',
                'uso',
                'telefono')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    list_display = (
        'entidad',
        'tipo',
        'uso',
        'telefono',)
    list_filter = (
        'entidad',
        'tipo',
        'uso')


@admin.register(DireccionElectronica)
class DireccionElectronicaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'mail',)
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    list_display = (
        'entidad',
        'mail',)
    list_filter = (
        'entidad',)


@admin.register(CalificacionAnual)
class CalificacionAnualAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'bombero',
        'periodo',
        'puntaje_en_numero',)
    list_filter = (
        'bombero',
        'periodo',)
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'periodo',
                'puntaje_en_numero',)
        }),
    )


@admin.register(NumeroOrden)
class NumeroOrdenAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_orden',
                'bombero',
                'vigencia_desde',)
        }),
        (_("Finalización de vigencia"), {
            'classes': ('collapse',),
            'fields': ('vigencia_hasta',),
        })
    )
    list_display = (
        'numero_orden',
        'bombero',
        'vigencia_desde',
        'vigencia_hasta',
    )
    list_filter = (
        'numero_orden',
        'bombero',
        'vigencia_desde',
        'vigencia_hasta',
    )
    date_hierarchy = 'vigencia_hasta'
    search_fields = (
        'numero_orden',
        'bombero.persona.apellido',
        'bombero.persona.nombre',
        'vigencia_desde',
        'vigencia_hasta',
    )
