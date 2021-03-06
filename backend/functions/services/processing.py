import io
import re
from datetime import datetime, timedelta
from typing import List, Callable, Union

import pandas as pd
import numpy as np  # нужно для генерируемой python функции

from django.core.files.base import ContentFile

from functions.models import Function
from functions.services.graph import draw_graph


class BadFunctionError(Exception):
    pass


def function_processing(function_id: int) -> None:
    # получение функции из бд
    function_obj = _get_function_object(function_id)

    if function_obj is False:
        return None

    # преобразуем строковую функцию в функцию python
    try:
        python_function = _string_to_python_function(function_obj.string_view)
    except BadFunctionError:
        return _set_status(function_obj, "Ошибка: Недопустимая функция")

    # получим данные для построения графиков

    # x_data - массив с датами
    x_data = _get_x_data(function_obj)

    # y_data - массив float
    try:
        y_data = _get_y_data(python_function, x_data)
    except SyntaxError:
        return _set_status(function_obj, "Ошибка: Недопустимая функция (возможно пропущен знак умножения)")

    # отрисовка графика
    graph_io = draw_graph(x_data, y_data)

    # сохраняем график на диске
    _save_graph(graph_io, function_obj)

    # обновить дату и статус
    _set_status(function_obj, "OK")


def _get_function_object(function_id: int) -> Union[Function, bool]:
    try:
        return Function.objects.get(
            pk=function_id
        )
    except Function.DoesNotExist:
        return False


def _string_to_python_function(string: str) -> Callable:
    """
    :param string: введенная пользователем функция
    :return: эквивалентная строке функция python
    """
    replacements = {
        'sin': 'np.sin',
        'cos': 'np.cos',
        'exp': 'np.exp',
        'sqrt': 'np.sqrt',
        '^': '**',
    }

    allowed_words = ['t', 'sin', 'cos', 'sqrt', 'exp']

    # проверка отсутствия недопустимых слов
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            raise BadFunctionError

    # замена допустимых функций на эквивалентные функции np и python
    for old, new in replacements.items():
        string = string.replace(old, new)

    # преобразование функции в строку
    def function(t):
        if t == 0:
            t = 0.1  # костыль
        return eval(string)

    return function


def _get_start(interval: int) -> datetime:
    return datetime.now() - timedelta(days=interval)


def _get_end() -> datetime:
    return datetime.now()


def _get_x_data(function_obj: Function) -> List[datetime]:
    HOUR_IN_DAY = 24

    # получим входные данные из бд
    interval = function_obj.interval
    dt = function_obj.dt

    # сформируем начало и конец интервала
    start = _get_start(interval)
    end = _get_end()

    # расчёт количества периодов генерации
    periods = round(interval * HOUR_IN_DAY / dt)

    # создание массива с датами
    x_data = pd.date_range(start, end, periods=periods).to_pydatetime()

    return x_data


def _get_y_data(function: Callable, x_data: List[datetime]) -> List[float]:
    if len(x_data) == 0:
        return []

    start = x_data[0]

    # приведем значение x к часам прошедшим с момента start
    y_data = [function(divmod((x - start).total_seconds(), 3600)[0]) for x in x_data]

    return y_data


def _set_status(function_obj: Function, status: str) -> None:
    function_obj.update_date = datetime.now()
    function_obj.status = status
    function_obj.save()


def _save_graph(graph_io: io.BytesIO, function_obj: Function) -> None:
    function_obj.graph.save("graph{}.png".format(function_obj.id), ContentFile(graph_io.getvalue()), save=True)
