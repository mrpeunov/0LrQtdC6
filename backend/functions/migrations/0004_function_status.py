# Generated by Django 3.2.6 on 2021-08-16 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0003_auto_20210816_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='function',
            name='status',
            field=models.CharField(default='Нет изображения', max_length=64, verbose_name='Статус'),
        ),
    ]
