from django.db import models


class Function(models.Model):
    function = models.CharField('Функция', max_length=128)
    graph = models.ImageField('График', blank=True)
    interval = models.IntegerField('Интервал t, дней')
    dt = models.IntegerField('Шаг t, часы')
    update_date = models.DateTimeField('Дата  обработки', auto_now=True)

    def save(self, *args, **kwargs):
        self.create_graph()
        super().save(*args, **kwargs)

    def create_graph(self):
        print("Создание графа", self.function)
