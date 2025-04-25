from django.db import models
from django.utils import timezone


class MailingRecipient(models.Model):
    """Создание модели получателя рассылки, которая будет хранить информацию о получателе"""

    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name}: <{self.email}>'


class Message(models.Model):
    """Модель для хранения сообщения с темой и телом сообщения."""

    subject = models.CharField(max_length=255, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Тело сообщения')

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Модель для хранения информации о рассылках"""

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    first_sent_at = models.DateTimeField(default=timezone.now, verbose_name='Дата и время первой отправки')
    ended_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    recipients = models.ManyToManyField('MailingRecipient', related_name='mailings', verbose_name='Получатели')

    def __str__(self):
        return f'Рассылка: {self.message.subject} - Статус: {self.get_status_display()}'
