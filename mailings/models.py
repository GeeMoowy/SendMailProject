from django.db import models


class MailingRecipient(models.Model):
    """Создание модели получателя рассылки, которая будет хранить информацию о получателе"""

    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name}: <{self.email}>'



