from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}

PERIODICITY = [
    ('once_a_day', 'once_a_day'),
    ('once_a_week', 'once_a_week'),
    ('once_a_month', 'once_a_month'),
]

STATUS = [
    ("start", "start"),
    ("finish", "finish"),
    ("created", "created"),
]


class Client(models.Model):
    email = models.CharField(max_length=100, unique=True, verbose_name='Email')
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.CharField(max_length=100, **NULLABLE, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return f'{self.fullname} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема письма')
    body = models.TextField(**NULLABLE, verbose_name='Содержимое письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mail(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тема рассылки")
    client = models.ManyToManyField(Client, verbose_name="Клиент")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name="Сообщение")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Начало")
    next_date = models.DateTimeField(default=timezone.now, verbose_name="Следующее")
    end_date = models.DateTimeField(default=timezone.now, verbose_name="Конец")
    periodicity = models.CharField(default="once_a_day", choices=PERIODICITY, verbose_name="Интервал")
    status = models.CharField(default="created", choices=STATUS, verbose_name="Статус")
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    permissions = [
        ("set_is_active", "Активация рассылки")
    ]


class Log(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')
    time_last_mailing = models.DateTimeField(auto_now=True, verbose_name='Время последней попытки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки', null=True)
    response = models.CharField(max_length=200, **NULLABLE, verbose_name="Ответ почтового сервера")

    def __str__(self):
        return f'Последняя попытка {self.time_last_mailing}, со статусом {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
