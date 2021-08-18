from django.db.models.signals import post_save
from django.dispatch import receiver
from functions.models import Function
from functions.services.celery_manager import call_create_graph
from django.db import transaction


@receiver(post_save, sender=Function)
def create_function(sender, instance, created, **kwargs):
    if created is True:
        # так как post save выполняется внутри транзакции
        # нужно выполнить после её завершения
        transaction.on_commit(lambda: call_create_graph(instance.pk))
