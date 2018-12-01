# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from actas.models import (
    Acta,

    ActaAscenso,
    ActaLicencia,
    ActaPase,
    ActaPremio,
    ActaReincorporacion,
    ActaRenuncia,

    Ascenso,
    Licencia,
    Pase,
    Premio,
    Reincorporacion,
    Renuncia,

    ActaSancion,
    Sancion,
)


@admin.register(Acta)
class ActaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_libro',
                'numero_folio',
                'numero_acta',
                'fecha_acta',
                'descripcion_acta',
                )
        }),
    )
    list_display = (
            'nombre_corto',
            'descripcion_acta',
    )
    list_filter = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
    )


class AscensoTabular(admin.TabularInline):
    model = Ascenso


@admin.register(ActaAscenso)
class ActaAscensoAdmin(admin.ModelAdmin):
    inlines = [
        AscensoTabular,
    ]
    list_display = (
        'get_acta',
        'fecha_efectiva',
    )
    list_filter = (
        'acta__fecha_acta',
        'fecha_efectiva',
    )
    search_fields = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
        'acta__descripcion_acta',
        'fecha_efectiva',
    )

    def get_acta(self, obj):
        return obj.acta.nombre_corto
    get_acta.short_description = _('Acta')


class LicenciaTabular(admin.TabularInline):
    model = Licencia


@admin.register(ActaLicencia)
class ActaLicenciaAdmin(admin.ModelAdmin):
    inlines = [
        LicenciaTabular,
    ]
    fieldsets = (
        (None, {
            'fields': (
                'acta',
                'fecha_efectiva',
            )
        }),
    )
    list_display = (
        'get_acta',
        'fecha_efectiva',
    )
    list_filter = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
    )
    search_fields = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
        'acta__descripcion_acta',
        'fecha_desde',
        'fecha_hasta',
        'bombero',
    )

    def get_acta(self, obj):
        return obj.acta.nombre_corto
    get_acta.short_description = _('Acta')


class PaseTabular(admin.TabularInline):
    model = Pase


@admin.register(ActaPase)
class ActaPaseAdmin(admin.ModelAdmin):
    inlines = [
        PaseTabular,
    ]
    list_display = (
        'get_acta',
        'fecha_efectiva',
    )
    list_filter = (
        'acta__fecha_acta',
        'fecha_efectiva',
    )
    search_fields = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
        'acta__descripcion_acta',
        'fecha_efectiva',
    )

    def get_acta(self, obj):
        return obj.acta.nombre_corto
    get_acta.short_description = _('Acta')


class PremioTabular(admin.TabularInline):
    model = Premio


@admin.register(ActaPremio)
class PremioAdmin(admin.ModelAdmin):
    inlines = [
        PremioTabular,
    ]
    list_display = (
        'get_acta',
        'fecha_efectiva',
    )
    list_filter = (
        'acta__fecha_acta',
        'fecha_efectiva',
    )
    search_fields = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
        'acta__descripcion_acta',
        'fecha_efectiva',
    )

    def get_acta(self, obj):
        return obj.acta.nombre_corto
    get_acta.short_description = _('Acta')


class ReincorporacionTabular(admin.TabularInline):
    model = Reincorporacion


@admin.register(ActaReincorporacion)
class ActaReincorporacionAdmin(admin.ModelAdmin):
    inlines = [
        ReincorporacionTabular,
    ]
    list_display = (
        'get_acta',
        'fecha_efectiva',
    )
    list_filter = (
        'acta__fecha_acta',
        'fecha_efectiva',
    )
    search_fields = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
        'acta__descripcion_acta',
        'fecha_efectiva',
    )

    def get_acta(self, obj):
        return obj.acta.nombre_corto
    get_acta.short_description = _('Acta')


class RenunciaTabular(admin.TabularInline):
    model = Renuncia


@admin.register(ActaRenuncia)
class ActaRenunciaAdmin(admin.ModelAdmin):
    inlines = [
        RenunciaTabular,
    ]
    list_display = (
        'get_acta',
        'fecha_efectiva',
    )
    list_filter = (
        'acta__fecha_acta',
        'fecha_efectiva',
    )
    search_fields = (
        'acta__numero_libro',
        'acta__numero_folio',
        'acta__numero_acta',
        'acta__fecha_acta',
        'acta__descripcion_acta',
        'fecha_efectiva',
    )

    def get_acta(self, obj):
        return obj.acta.nombre_corto
    get_acta.short_description = _('Acta')


class SancionTabular(admin.TabularInline):
    model = Sancion


@admin.register(ActaSancion)
class ActaSancionAdmin(admin.ModelAdmin):
    inlines = [
        SancionTabular,
    ]
    '''
    list_display = (
            'acta',
            'fecha_acta',
            'fecha_incidente',
    )
    list_filter = (
            'fecha_acta',
            'fecha_incidente',
    )
    search_fields = (
            'numero_libro',
            'numero_folio',
            'numero_acta',
            'fecha_acta',
            'descripcion_acta',
            'fecha_incidente',
    )

    def acta(self, obj):
        return obj.nombre_corto
    acta.short_description = _('Acta')
    '''