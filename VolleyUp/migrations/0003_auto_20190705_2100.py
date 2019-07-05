# Generated by Django 2.2.2 on 2019-07-05 19:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('VolleyUp', '0002_auto_20190705_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 5, 20, 30, 35, 348977, tzinfo=utc), verbose_name='Koniec treningu'),
        ),
        migrations.AlterField(
            model_name='uprawnienia',
            name='training',
            field=models.ManyToManyField(related_name='uprawnienia', to='VolleyUp.Training', verbose_name='Trening'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uprawnienia',
            field=models.ManyToManyField(related_name='users_upr', to='VolleyUp.Uprawnienia', verbose_name='Uprawnienia'),
        ),
    ]