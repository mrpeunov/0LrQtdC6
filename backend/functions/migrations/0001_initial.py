# Generated by Django 3.2.6 on 2021-08-15 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(max_length=128, verbose_name='Функция')),
                ('graph', models.ImageField(upload_to='', verbose_name='График')),
                ('interval', models.IntegerField(verbose_name='Интервал t, дней')),
                ('dt', models.IntegerField(verbose_name='Шаг t, часы')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления, обработки')),
            ],
        ),
    ]
