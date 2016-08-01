from django.contrib import admin
from personas.models import Persona, Bombero, Parentesco
from django.utils.translation import ugettext as _


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'apellido',
                'nombre',
                'tipo_documento',
                'documento',
                'fecha_nacimiento',)
        }),
        (_('¿Fallecido?'), {
            'classes': ('collapse',),
            'fields': ('fecha_desceso',),
        }),
    )
    list_display = (
        'apellido',
        'nombre',
        'tipo_documento',
        'documento',
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
        'fecha_desceso',)
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Bombero)
class BomberoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'apellido',
                'nombre',
                'tipo_documento',
                'documento',
                'fecha_nacimiento',
                'foto',
                'lugar_nacimiento',
                'estado_civil',)
        }),
        (_('¿Fallecido?'), {
            'classes': ('collapse',),
            'fields': ('fecha_desceso',),
        }),
    )
    list_display = (
        'apellido',
        'nombre',
        'tipo_documento',
        'documento',
        'fecha_nacimiento')
    search_fields = (
        'apellido',
        'nombre',
        'documento',
        'lugar_nacimiento__nombre')
    list_filter = (
        'apellido',
        'lugar_nacimiento')
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Parentesco)
class ParentescoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    raw_id_fields = (
        ('Bombero.apellido',
            'Bombero.nombre'),
        ('Persona.apellido',
            'Persona.nombre'),)
    list_display = (
        ('Bombero.apellido',
            'Bombero.nombre'),
        ('Persona.apellido',
            'Persona.nombre'),)
    search_fields = (
        'Bombero.apellido',
        'Bombero.nombre',
        'Persona.apellido',
        'Persona.nombre',)
    list_filter = (
        'Bombero.apellido',
        'Bombero.lugar_nacimiento',)
    date_hierarchy = 'Bombero.fecha_nacimiento'