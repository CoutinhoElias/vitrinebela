from django.conf import settings
from django.db import models
from django.utils import timezone


class Booking(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário')
    title = models.CharField('evento', max_length=128)
    start = models.DateField('inicio')
    end = models.DateField('fim')
    created_on = models.DateTimeField('solicitado em', default=timezone.now)
    authorized = models.BooleanField('autorizado', default=False)
    color = models.CharField('cor', max_length=15)

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ('-start',)

    def __str__(self):
        return self.title