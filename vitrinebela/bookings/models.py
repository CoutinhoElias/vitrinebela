# from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from vitrinebela.accounts.models import User


class Booking(models.Model):
    # CHOICES NO MODELS VAI TER UMA LISTAGEM NO ADMIN
    CORES_CHOICES = (
        ('red', 'red'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('black', 'black'),
        ('yellow', 'yellow')
    )

    allday = models.BooleanField('Dia inteiro', default=False)
    title = models.CharField('evento', max_length=128)
    start = models.DateTimeField('inicio')
    end = models.DateTimeField('fim')
    created_on = models.DateTimeField('solicitado em', default=timezone.now)
    authorized = models.BooleanField('autorizado', default=False)
    editable = models.BooleanField('Editavel', default=True) #True permite o user arrastar e soltar para qualquer data, False não permite
    color = models.CharField('cor', max_length=15, choices=CORES_CHOICES, default='blue')
    overlap = models.BooleanField('Sobrepor', default=True) #Áreas vermelhas onde nenhum evento pode ser descartado (Período que não pode receber nenhum agendamento)
    holiday = models.BooleanField('Feriado')
    participants = models.ManyToManyField(User, related_name="item_participantes")
    #rendering: 'background' Áreas onde "Reunião" deve ser descartado (Sem permissão de Incluir/Editar/Excluir o evendo)
    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ('-start',)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('scheduling:agendamento')