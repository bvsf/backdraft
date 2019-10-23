from django.contrib import admin
from django.utils.translation import ugettext as _
from salud.models import (
    Alergenos,
    Alergicos,
    ObraSocial,
    PlanMedico,
    Clinica,
    MedicoCabecera,
    CoberturaMedica)


@admin.register(Alergenos)
class AlergenosAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'nombre_alergeno',)
        }),
    )
    list_display = (
        'nombre_alergeno',)
    search_fields = (
        'nombre_alergeno',)


@admin.register(Alergicos)
class AlergicosAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'alergeno',
                'observaciones')
        }),
    )
    list_display = (
        'bombero',
        'alergeno',
        'observaciones')
    search_fields = (
        'bombero',
        'alergeno')


@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'institucion',
                )
        }),
    )
    list_display = (
        'institucion',)
    search_fields = (
        'institucion__razon_social',)


@admin.register(PlanMedico)
class PlanMedicoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'obraSocial',
                'plan',
                'descripcion'
                )
        }),
    )
    list_display = (
        'obraSocial',
        'plan',
        'descripcion')
    search_fields = (
        'obraSocial__institucion__razon_social',
        'plan',
        'descripcion')


@admin.register(Clinica)
class Clinica(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'institucion',)
        }),
    )
    list_display = (
        'institucion',)
    search_fields = (
        'institucion__razon_social',)


@admin.register(MedicoCabecera)
class MedicoCabeceraAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'apellido',
                'nombre',
                'especialidad',
                'nroMatricula')
        }),
    )
    list_display = (
        'apellido',
        'nombre',
        'especialidad',
        'nroMatricula')
    search_fields = (
        'apellido',
        'nombre',
        'especialidad',
        'nroMatricula')


@admin.register(CoberturaMedica)
class CoberturaMedicaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'nroAfiliado',
                'planMedico',
                'medicoCabecera',
                'clinica',
                'fechaInicio')
        }),
        (_('¿Cobertura finalizada?'), {
            'classes': ('collapse',),
            'fields': ('fechaFin',),
        }),
        (_('¿Observaciones?'), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
        }),

    )
    list_display = (
        'bombero',
        'nroAfiliado',
        'planMedico',
        'medicoCabecera',
        'clinica',
        'fechaInicio',
        'fechaFin')
    search_fields = (
        'planMedico__obraSocial__institucion__razon_social',
        'planMedico__descripcion',
        'clinica__institucion__razon_social',
        'medicoCabecera__persona__nombre',
        'medicoCabecera__persona__apellido',
        'medicoCabecera__persona__documento',
        'medicoCabecera__nroMatricula',
        'bombero__persona__apellido',
        'bombero__persona__nombre',
        'bombero__persona__documento',
        'nroAfiliado')