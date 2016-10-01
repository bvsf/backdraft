from django.contrib import admin
from django.utils.translation import ugettext as _
from personas.models import (
    Persona,
    Bombero,
    DireccionPostal,
    DireccionWeb,
    Telefono,
    DireccionElectronica,
    Parentesco)


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
        'documento',)
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
                'foto',
                'estado_civil',
                'lugar_nacimiento',
                )
        }),
    )
    list_display = (
        'numero_credencial',
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
        'persona__documento')


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
