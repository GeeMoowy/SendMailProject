from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Фото', null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='Страна', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
