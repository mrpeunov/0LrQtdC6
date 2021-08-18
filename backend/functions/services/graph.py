import io
from datetime import datetime
from typing import List

from matplotlib import pyplot as plt, pylab
from matplotlib import dates


def draw_graph(x_data: List[datetime], y_data: List[float]):
    """
    x_data - массив дат
    y_data - массив float
    """

    # Преобразуем даты в числовой формат
    x_data_float = dates.date2num(x_data)

    # Вызовем subplot явно, чтобы получить экземпляр класса AxesSubplot,
    # из которого будем иметь доступ к осям
    axes = pylab.subplot(1, 1, 1)

    # если разница между начало и концом больше года
    if divmod((x_data[0]-x_data[-1]).total_seconds(), 31536000)[0] >= 1:
        # дата подписывается как год
        axes.xaxis.set_major_formatter(dates.DateFormatter("%Y"))
    else:
        # дата подписывается как день и месяц
        axes.xaxis.set_major_formatter(dates.DateFormatter("%M%D"))

    # Отобразим данные
    pylab.plot_date(x_data_float, y_data, fmt="b-")

    # Изменим левую границу
    if len(x_data) > 0:
        pylab.xlim(xmin=dates.date2num(x_data[0]))

    pylab.grid()

    # выгрузим изображение из matplotlib
    result_image = io.BytesIO()
    plt.savefig(result_image, format="png")
    plt.clf()

    return result_image
