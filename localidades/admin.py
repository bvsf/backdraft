from django.contrib import admin
from localidades.models import (
    Pais, Provincia, Localidad)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = [
        'nombre',
        'abreviatura']
    search_fields = [
        'nombre',
        'abreviatura']


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = [
        'nombre',
        'abreviatura',
        'pais']
    search_fields = [
        'nombre',
        'abreviatura',
        'pais__nombre',
        'pais__abreviatura']
    list_filter = ['pais']


@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = [
        'nombre',
        'abreviatura',
        'codigo_postal',
        'provincia']
    search_fields = [
        'nombre',
        'abreviatura',
        'codigo_postal',
        'provincia__nombre',
        'provincia__abreviatura']
    list_filter = ['provincia']
