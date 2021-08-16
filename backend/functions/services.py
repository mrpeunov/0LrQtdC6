import re
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

from functions.models import Function


def create_graph(function_id):
    # получим информацию о функции из БД
    function = get_function(function_id)

    # преобразуем строковую функцию в функцию python
    try:
        python_function = string_to_python_function(function.string_view)
    except ValueError:
        return set_bad_status(function)

    # подготовим значения начала и конца функции
    start = get_start(function.interval)
    finish = get_finish()

    # генериуем точки
    points = generate_points(start, finish, function.interval, function.dt)

    # рисуем график
    draw_graph(points, python_function, start, finish)

    # сохраняем график на диске
    save_graph()

    # актуализируем дату
    function.update_date = datetime.now()


def string_to_python_function(string):
    """
    :param string: введенная пользователем функция
    :return: эквивалентая строке функция python
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
            raise ValueError(
                '"{}" запрещено использовать в математическом выражении'.format(word)
            )

    # замена допустимых функций на эквивалентные функции np и python
    for old, new in replacements.items():
        string = string.replace(old, new)

    # преобразование функции в строку
    def function(t):
        return eval(string)

    return function


def get_function(function_id):
    return Function.objects.get(
        pk=function_id
    )


def set_bad_status(function):
    function.status = 'Плохая функция'
    function.save()


def draw_graph(points, function, start, finish):
    plt.plot(points, function(points))
    plt.xlim(start, finish)
    # plt.show()


def get_start(interval):
    return float(datetime.now() - interval)


def get_finish():
    return float(datetime.now())


def generate_points(start, finish, interval, dt):
    return np.linspace(start, finish, round(interval/dt))


def save_graph():
    plt.savefig('saved_figure.png')
