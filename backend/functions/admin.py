from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Function
from .services.celery_manager import call_create_graph
from .tasks import update_graph


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ['string_view', 'get_graph', 'interval', 'dt', 'update_date']
    exclude = ['graph', 'status']
    readonly_fields = ['update_date']
    actions = ['update_graph']

    @admin.action(description='Обновить')
    def update_graph(self, request, queryset):
        """при выборе действия обновить, обновляет графики функций"""
        for function_item in queryset:
            call_create_graph(function_item.pk)

    def get_actions(self, request):
        """убираем действие удаления объекта"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_graph(self, obj):
        """вывод изображения и статуса с ошибкой"""
        if obj.status == "OK" and obj.graph:
            result = '<img src={} width="400" height="400">'.format(obj.graph.url)
        else:
            result = '<p>{}</p>'.format(obj.status)

        return mark_safe(result)
