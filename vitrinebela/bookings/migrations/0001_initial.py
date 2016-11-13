# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-12 13:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=128, verbose_name='evento')),
                ('date', models.DateField(verbose_name='data')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='solicitado em')),
                ('authorized', models.BooleanField(default=False, verbose_name='autorizado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name_plural': 'reservas',
                'ordering': ('-date',),
                'verbose_name': 'reserva',
            },
        ),
    ]
