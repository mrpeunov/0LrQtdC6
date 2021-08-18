from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Function
from .services.processing import function_processing
from .tasks import update_graph


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ['string_view', 'get_graph', 'interval', 'dt', 'update_date']
    readonly_fields = ['graph', 'status']
    actions = ['update_graph']

    @admin.action(description='Обновить')
    def update_graph(self, request, queryset):
        for function_item in queryset:
            result = update_graph.apply_async((function_item.pk, ), countdown=3)
            result.get()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_graph(self, obj):
        if obj.status == "OK":
            result = '<img src={} width="400" height="400">'.format(obj.graph.url)
        else:
            result = '<p>{}</p>'.format(obj.status)

        return mark_safe(result)
