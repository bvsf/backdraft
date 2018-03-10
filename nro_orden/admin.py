from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils import timezone
from daterange_filter.filter import DateRangeFilter
from django.contrib.admin.filters import DateFieldListFilter
from nro_orden.models import NumeroOrden


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
