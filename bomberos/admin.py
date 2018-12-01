# -*- coding: UTF-8 -*-
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from bomberos.models import (
    Bombero,
    Parentesco,
    Estudio,
    Empleo,
    CalificacionAnual,
    NumeroOrden,
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
        'nro_legajo',
        'numero_credencial',
        'fecha_vencimiento',
        'nombre_completo',
        'dni',
        'sangre',
        'get_grado_ultimo_ascenso',
        'antiguedad_bombero',
        'antiguedad_cuartel',
    )

    def nro_legajo(self, obj):
        return obj.pk
    nro_legajo.short_description = _('Legajo')

    def nombre_completo(self, obj):
        return obj.persona.nombre_completo
    nombre_completo.short_description = _('Apellido y Nombre')

    def sangre(self, obj):
        return obj.persona.sangre
    sangre.short_description = _('Grupo Sanguíneo')

    def dni(self, obj):
        return obj.persona.dni
    dni.short_description = _('Documento')

    def get_grado_ultimo_ascenso(self, obj):
        try:
            return obj.get_grado_ultimo_ascenso.nombre
        except AttributeError:
            return None
    get_grado_ultimo_ascenso.short_description = _("Grado")

    def antiguedad_bombero(self, obj):
        if obj.antiguedad_bombero:
            return _("{} años").format(
                obj.antiguedad_bombero,
            )
        else:
            return None
    antiguedad_bombero.short_description = _("Antigüedad como Bombero")

    def antiguedad_cuartel(self, obj):
        if obj.antiguedad_cuartel:
            return _("{} años").format(
                obj.antiguedad_cuartel,
            )
        else:
            return None
    antiguedad_cuartel.short_description = _("Antigüedad al Cuartel")

    search_fields = (
        'persona__apellido',
        'persona__primer_nombre',
        'persona__segundo_nombre',
        'persona__tercer_nombre',
        'persona__documento',
        'persona__nro_cuit',
    )
    list_filter = (
        'persona__apellido',
        'persona__fecha_nacimiento',
        'persona__tipo_documento',
        'persona__genero',
        'persona__grupo_sanguineo',
        'persona__factor_sanguineo',
        'persona__fecha_desceso',
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
        ('vigencia_hasta', DateRangeFilter),
    )
    date_hierarchy = 'vigencia_hasta'
    search_fields = (
        'numero_orden',
        'bombero.persona.apellido',
        'bombero.persona.nombre',
        'vigencia_desde',
        'vigencia_hasta',
    )


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

