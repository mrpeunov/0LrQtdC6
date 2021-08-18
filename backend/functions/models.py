from django.db import models


class Function(models.Model):
    string_view = models.CharField('Функция', max_length=128)
    graph = models.ImageField('График', blank=True, upload_to='graphs')
    interval = models.IntegerField('Интервал t, дней')
    dt = models.IntegerField('Шаг t, часы')
    status = models.CharField('Статус', max_length=64, default='Нет изображения')
    update_date = models.DateTimeField('Дата  обработки', blank=True, null=True)

    def __str__(self):
        return "Функция {}".format(self.string_view)

    class Meta:
        verbose_name = "Функция"
        verbose_name_plural = "Функции"
