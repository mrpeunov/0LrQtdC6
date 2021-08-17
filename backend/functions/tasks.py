from celery import shared_task
from functions.services.processing import function_processing


@shared_task
def update_graph(function_id):
    function_processing(function_id)
    return True
