from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from medios_contacto.models import (
    DireccionPostal, DireccionWeb, Telefono)


@admin.register(DireccionPostal)
class DireccionPostalAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
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
    list_filter = (
        'calle',
        'localidad')


@admin.register(DireccionWeb)
class DireccionWebAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo',
                'direccion')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))


@admin.register(Telefono)
class TelefonoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo',
                'telefono')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))