from functions.tasks import update_graph


def call_create_graph(function_id: int) -> None:
    """вызов операции celery с ожиданием результата"""
    result = update_graph.apply_async((function_id,), countdown=3)
    result.get()
