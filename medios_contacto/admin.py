from django.contrib import admin
from medios_contacto.models import DireccionPostal


@admin.register(DireccionPostal)
class DireccionPostalAdmin(admin.ModelAdmin):
    search_fields = (
        'calle',
        'numero',
        'piso',
        'departamento',
        'localidad__nombre')
