from django.contrib import admin
from .models import Function


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ['function', 'graph', 'interval', 'dt', 'update_date']
    readonly_fields = ['graph']
    actions = ['update_graph']

    @admin.action(description='Обновить')
    def update_graph(self, request, queryset):
        for function_item in queryset:
            function_item.create_graph()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
