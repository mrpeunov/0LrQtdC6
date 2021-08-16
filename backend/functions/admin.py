from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Function
# from .services import create_graph


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ['string_view', 'get_graph', 'interval', 'dt', 'update_date']
    readonly_fields = ['graph', 'status']
    actions = ['update_graph']

    @admin.action(description='Обновить')
    def update_graph(self, request, queryset):
        for function_item in queryset:
            pass
            # create_graph(function_item.pk)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_graph(self, obj):
        result = '<p>{}</p>'.format(obj.status)

        if obj.graph:
            result = '<img src={} width="400" height="400">'.format(obj.graph.url)

        return mark_safe(result)
