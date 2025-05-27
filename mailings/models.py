from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class MailingRecipient(models.Model):
    """Создание модели получателя рассылки, которая будет хранить информацию о получателе"""

    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        permissions = [
            ('can_view_all_recipients', 'Может просматривать всех получателей'),
        ]

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
        ('disabled', 'Отключена'),
    ]

    first_sent_at = models.DateTimeField(default=timezone.now, verbose_name='Дата и время первой отправки')
    ended_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    recipients = models.ManyToManyField('MailingRecipient', related_name='mailings', verbose_name='Получатели')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        permissions = [
            ('can_view_all_mailing', 'Может просматривать все рассылки'),
            ('can_disable_mailing', 'Может отключать рассылки'),
        ]

    def __str__(self):
        return f'Рассылка: {self.message.subject} - Статус: {self.get_status_display()}'


class SendingAttempt(models.Model):
    """Модель для хранения информации о попытках отправки рассылки."""

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=20, choices=[
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ], verbose_name='Статус')
    response = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='sending_attempts')

    def __str__(self):
        return f'Попытка отправки: {self.status} - {self.attempt_time}'
