from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    email_token = models.CharField(max_length=20, verbose_name='Токен', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')
    # fullname = models.CharField(max_length=30, verbose_name='FIO', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
