from django.contrib import admin
from tipos_documento.models import TipoDocumento


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'abreviatura',
        'tipo')
    list_display_links = None
    list_editable = (
        'abreviatura',
        'tipo')
    search_fields = [
        'abreviatura',
        'tipo']
    actions_on_bottom = True
