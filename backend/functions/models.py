from django.db import models


class Function(models.Model):
    string_view = models.CharField('Функция', max_length=128)
    graph = models.ImageField('График', blank=True)
    interval = models.IntegerField('Интервал t, дней')
    dt = models.IntegerField('Шаг t, часы')
    status = models.CharField('Статус', max_length=64, default='Нет изображения')
    update_date = models.DateTimeField('Дата  обработки', auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("Создание графа", self.string_view)
        # create_graph(self.pk)

    # def create_graph(self):
    #     # print("Создание графа", self.string_view)

