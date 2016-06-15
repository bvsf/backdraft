from django.contrib import admin
from personas.models import Persona


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
        'tipo_documento')
    date_hierarchy = 'fecha_nacimiento'
    exclude = (
        'borrado',
        'historico',
        'usuario_creador',
        'fecha_creacion',
        'usuario_modificador',
        'fecha_modificacion')
