from django.contrib import admin
from personas.models import Persona, Bombero, Fallecido


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'apellido',
        'nombre',
        'tipo_documento',
        'documento',
        'fecha_nacimiento')
    search_fields = (
        'apellido',
        'nombre',
        'documento',)
    list_filter = (
        'apellido',
        'fecha_nacimiento',
        'tipo_documento',)
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Bombero)
class BomberoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
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


@admin.register(Fallecido)
class FallecidoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'apellido',
        'nombre',
        'tipo_documento',
        'documento',
        'fecha_nacimiento',
        'fecha_desceso')
    search_fields = (
        'apellido',
        'nombre',
        'documento',)
    list_filter = (
        'apellido',
        'fecha_nacimiento',
        'tipo_documento',
        'fecha_desceso')
    date_hierarchy = 'fecha_desceso'
