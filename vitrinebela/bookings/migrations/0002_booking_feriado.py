# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-01 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='feriado',
            field=models.BooleanField(default=False, verbose_name='Feriado'),
            preserve_default=False,
        ),
    ]