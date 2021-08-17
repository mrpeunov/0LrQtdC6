import re
from datetime import datetime, timedelta

import pandas as pd
import numpy as np  # нужно для генерируемой python функции

from django.core.files.base import ContentFile

from functions.models import Function
from functions.services.graph import draw_graph


class BadFunctionError(Exception):
    pass


def function_processing(function_id):
    print("Из точки A")
    # получение функции из бд
    function_obj = _get_function_object(function_id)

    # преобразуем строковую функцию в функцию python
    try:
        python_function = _string_to_python_function(function_obj.string_view)
    except BadFunctionError:
        return _set_status(function_obj, "Введенная функция не может быть преобразована в математическое выражение")

    # получим данные для построения графиков
    # x_data - массив с датами, y_data - массив float
    x_data = _get_x_data(function_obj)
    y_data = _get_y_data(python_function, x_data)

    # отрисовка графика
    graph_io = draw_graph(x_data, y_data)

    # сохраняем график на диске
    _save_graph(graph_io, function_obj)

    # обновить дату и статус
    _set_status(function_obj, "OK")

    print("В точку B")


def _get_function_object(function_id):
    return Function.objects.get(
        pk=function_id
    )


def _string_to_python_function(string):
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
        return eval(string)

    return function


def _get_start(interval):
    return datetime.now() - timedelta(days=interval)


def _get_end():
    return datetime.now()


def _get_x_data(function_obj):
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


def _get_y_data(function, x_data):
    if len(x_data) == 0:
        return []

    start = x_data[0]

    # приведем значение x к часам прошедшим с момента start
    y_data = [function(divmod((x - start).total_seconds(), 3600)[0]) for x in x_data]

    return y_data


def _set_status(function_obj, status):
    function_obj.update_date = datetime.now()
    function_obj.status = status
    function_obj.save()


def _save_graph(graph_io, function_obj):
    function_obj.graph.save("graph{}.png".format(function_obj.id), ContentFile(graph_io.getvalue()), save=True)
