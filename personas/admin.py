# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from personas.models import (
    Persona,
    DireccionPostal,
    DireccionWeb,
    Telefono,
    DireccionElectronica,
    Institucion,
    Cuartelero,
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


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo_cuit',
                'nro_cuit',
                'apellido',
                'primer_nombre',
                'segundo_nombre',
                'tercer_nombre',
                'tipo_documento',
                'documento',
                'grupo_sanguineo',
                'factor_sanguineo',
                'fecha_nacimiento',
                'genero')
        }),
        (_('¿Fallecido?'), {
            'classes': ('collapse',),
            'fields': ('fecha_desceso',),
        }),
    )
    list_display = (
        'nombre_completo',
        'dni',
        'genero',
        'sangre',
        'fecha_nacimiento',
        'fecha_desceso',)
    search_fields = (
        'apellido',
        'primer_nombre',
        'segundo_nombre',
        'tercer_nombre',
        'documento',
        'nro_cuit',
    )
    list_filter = (
        'apellido',
        'fecha_nacimiento',
        'tipo_documento',
        'genero',
        'grupo_sanguineo',
        'factor_sanguineo',
        'fecha_desceso',)
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Cuartelero)
class CuarteleroAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'persona',),
        }),
    )
    list_display = (
        '__str__',
        'dni',
        'fecha_nacimiento',
        'sangre',
    )
    search_fields = (
        'persona__apellido',
        'persona__primer_nombre',
        'persona__segundo_nombre',
        'persona__tercer_nombre',
        'persona__documento',
        'persona__nro_cuit',
    )
    list_filter = (
        'persona__apellido',
        'persona__fecha_nacimiento',
        'persona__tipo_documento',
        'persona__genero',
        'persona__grupo_sanguineo',
        'persona__factor_sanguineo',
        'persona__fecha_desceso',
    )


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
