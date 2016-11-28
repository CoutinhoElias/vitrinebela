from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Booking(models.Model):

    CORES_CHOICES = (
        ('red', 'red'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('black', 'black'),
    )

    user = models.ForeignKey(User)
    allday = models.BooleanField('Dia inteiro', default=False)
    title = models.CharField('evento', max_length=128)
    start = models.DateTimeField('inicio')
    end = models.DateTimeField('fim')
    created_on = models.DateTimeField('solicitado em', default=timezone.now)
    authorized = models.BooleanField('autorizado', default=False)
    editable = models.BooleanField('Editavel', default=True)
    color = models.CharField('cor', max_length=15, choices=CORES_CHOICES, default='blue')
    backgroundColor = models.CharField('Cor de Fundo', max_length=15, choices=CORES_CHOICES, default='blue')

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ('-start',)

    def __str__(self):
        return self.title