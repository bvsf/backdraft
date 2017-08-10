from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.admin.filters import DateFieldListFilter
from personas.models import (
    Persona,
    Bombero,
    DireccionPostal,
    DireccionWeb,
    Telefono,
    DireccionElectronica,
    Parentesco,
    Estudio,
    Empleo,
    Institucion,
    CalificacionAnual,
    NumeroOrden,
)


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo_cuit',
                'nro_cuit',
                'razon_social',
                )
        }),
    )
    list_display = (
        'tipo_cuit',
        'nro_cuit',
        'razon_social',
    )
    search_fields = (
        'nro_cuit',
        'razon_social',
    )


@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'establecimiento',
                'nivel',
                'titulo',
                'estado',
                'periodo_desde',
                'periodo_hasta',
                )
        }),
        (_('Descripcion'), {
            'classes': ('collapse',),
            'fields': ('descripcion',),
        }),
    )
    list_display = (
        'periodo',
        'establecimiento',
        'bombero',
    )
    search_fields = (
        'bombero__persona__apellido',
        'bombero__persona__nombre',
        'bombero__persona__documento',
        'bombero__persona__nro_cuit',
        'establecimiento__razon_social',
        'establecimiento__nro_cuit',
        'nivel',
        'estado',
        'titulo',
    )
    list_filter = (
        'bombero',
        'establecimiento',
        'nivel',
        'estado',
        'titulo',
    )
    date_hierarchy = 'periodo_desde'

    def periodo(self, obj):
        return obj.periodo
    periodo.short_description = _('Periodo')


@admin.register(Empleo)
class EmpleoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'empresa',
                'titulo',
                'periodo_desde',
                'periodo_hasta',
                )
        }),
        (_('Descripcion'), {
            'classes': ('collapse',),
            'fields': ('descripcion',),
        }),
    )
    list_display = (
        'periodo',
        'empresa',
        'bombero',
    )
    search_fields = (
        'bombero__persona__apellido',
        'bombero__persona__nombre',
        'bombero__persona__documento',
        'bombero__persona__nro_cuit',
        'empresa__razon_social',
        'empresa__nro_cuit',
        'titulo',
    )
    list_filter = (
        'bombero',
        'empresa',
    )
    date_hierarchy = 'periodo_desde'

    def periodo(self, obj):
        return obj.periodo
    periodo.short_description = _('Periodo')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'tipo_cuit',
                'nro_cuit',
                'apellido',
                'nombre',
                'tipo_documento',
                'documento',
                'grupo_sanguineo',
                'factor_sanguineo',
                'fecha_nacimiento',)
        }),
        (_('¿Fallecido?'), {
            'classes': ('collapse',),
            'fields': ('fecha_desceso',),
        }),
    )
    list_display = (
        'nombre_completo',
        'dni',
        'sangre',
        'fecha_nacimiento',
        'fecha_desceso',)
    search_fields = (
        'apellido',
        'nombre',
        'documento',
        'nro_cuit',
    )
    list_filter = (
        'apellido',
        'fecha_nacimiento',
        'tipo_documento',
        'grupo_sanguineo',
        'factor_sanguineo',
        'fecha_desceso',)
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Bombero)
class BomberoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'persona',
                'numero_credencial',
                'fecha_vencimiento',
                'foto',
                'estado_civil',
                'lugar_nacimiento',
                )
        }),
    )
    list_display = (
        'numero_credencial',
        'fecha_vencimiento',
        'nombre_completo',
        'dni',
        'sangre',
    )

    def nombre_completo(self, obj):
        return obj.persona.nombre_completo
    nombre_completo.short_description = _('Apellido y Nombre')

    def sangre(self, obj):
        return obj.persona.sangre
    sangre.short_description = _('Grupo Sanguíneo')

    def dni(self, obj):
        return obj.persona.dni
    dni.short_description = _('Documento')

    search_fields = (
        'persona__apellido',
        'persona__nombre',
        'persona__documento',
        'persona__nro_cuit',
    )


@admin.register(Parentesco)
class ParentescoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'bombero',
        'familiar',
        'parentesco',)
    search_fields = (
        'bombero.persona.apellido',
        'bombero.persona.nombre',
        'familiar.apellido',
        'familiar.nombre',)


@admin.register(DireccionPostal)
class DireccionPostalAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
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
    list_display = (
        'entidad',
        'direccion_completa',
    )
    list_filter = (
        'entidad',
        'uso',
        'localidad')


@admin.register(DireccionWeb)
class DireccionWebAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'tipo',
                'uso',
                'direccion')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    list_display = (
        'entidad',
        'tipo',
        'uso',
        'direccion')
    list_filter = (
        'entidad',
        'tipo',
        'uso')


@admin.register(Telefono)
class TelefonoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'tipo',
                'uso',
                'telefono')
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    list_display = (
        'entidad',
        'tipo',
        'uso',
        'telefono',)
    list_filter = (
        'entidad',
        'tipo',
        'uso')


@admin.register(DireccionElectronica)
class DireccionElectronicaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'entidad',
                'mail',)
            }),
        (_("Observaciones"), {
            'classes': ('collapse',),
            'fields': ('observaciones',),
            }))
    list_display = (
        'entidad',
        'mail',)
    list_filter = (
        'entidad',)


@admin.register(CalificacionAnual)
class CalificacionAnualAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'bombero',
        'periodo',
        'puntaje_en_numero',)
    list_filter = (
        'bombero',
        'periodo',)
    fieldsets = (
        (None, {
            'fields': (
                'bombero',
                'periodo',
                'puntaje_en_numero',)
        }),
    )


# https://djangosnippets.org/snippets/10566/
class DateFieldListFilterOrNull(DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_isnull = '%s__isnull' % (field_path,)
        super(DateFieldListFilterOrNull, self).__init__(field, request, params, model, model_admin, field_path)
        self.links = self.links + (
            (_("Sólo los Activos"), {
                self.lookup_kwarg_isnull: 'True',
            }),
            (_("Sólo los Inactivos"), {
                self.lookup_kwarg_isnull: 'False',
            }),
        )

    def expected_parameters(self):
        return super(DateFieldListFilterOrNull, self).expected_parameters() + [self.lookup_kwarg_isnull, ]


@admin.register(NumeroOrden)
class NumeroOrdenAdmin(admin.ModelAdmin):
    """
    Acciones con parametros
    http://agiliq.com/blog/2014/08/passing-parameters-to-django-admin-action/
    Da un error que dice "No se ha seleccionado ninguna accion :|

    class CierreActionForm(ActionForm):
        fecha_cierre = forms.DateField()

    def cerrar_vigencia(modeladmin, request, queryset):
        fecha = request.POST.get('fecha_cierre', timezone.now())
        print("Action!!")
        if not isinstance(fecha, datetime):
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError(
                    {'vigencia_hasta':
                         _("La fecha de cierre de vigencia no es válida, debe tener el formato 'YYYY-MM-DD'.")})
        queryset.update(vigencia_hasta=fecha)
        modeladmin.message_user(
            request,
            _("Se cerraron satisfactoriamente las vigencias a {0} Bomberos").format(queryset.count()),)
    cerrar_vigencia.short_description = _("Cerrar vigencia de los bomberos seleccionados")

    action_form = CierreActionForm
    """
    def cerrar_vigencia(modeladmin, request, queryset):
        queryset.update(vigencia_hasta=timezone.now())
        modeladmin.message_user(
            request,
            _("Se cerraron satisfactoriamente las vigencias a {0} Bomberos").format(queryset.count()), )
    cerrar_vigencia.short_description = _("Cerrar vigencia de los bomberos seleccionados")

    actions = [cerrar_vigencia]
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'numero_orden',
                'bombero',
                'vigencia_desde',)
        }),
        (_("Finalización de vigencia"), {
            'classes': ('collapse',),
            'fields': ('vigencia_hasta',),
        })
    )
    list_display = (
        'numero_orden',
        'bombero',
        'vigencia_desde',
        'vigencia_hasta',
    )
    list_filter = (
        'numero_orden',
        'bombero',
        'vigencia_desde',
        ('vigencia_hasta', DateFieldListFilterOrNull),
    )
    date_hierarchy = 'vigencia_hasta'
    search_fields = (
        'numero_orden',
        'bombero.persona.apellido',
        'bombero.persona.nombre',
        'vigencia_desde',
        'vigencia_hasta',
    )

