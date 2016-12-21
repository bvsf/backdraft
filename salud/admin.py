from django.contrib import admin
from django.utils.translation import ugettext as _
from salud.models import (
    Alergenos,
    Alergicos
)


@admin.register(Alergenos)
class AlergenosAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'nombre_alergeno'
            )
        }),
    )
    list_display = (
        'nombre_alergeno'
    )
    search_fields = (
        'nombre_alergeno'
    )


@admin.register(Alergicos)
class AlergicosAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'alergeno',
                'observaciones'
                )
        }),
    )
    list_display = (
        'bombero',
        'alergeno',
        'observaciones'
    )
    search_fields = (
        'bombero',
        'alergeno'
    )