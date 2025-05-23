from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailings.models import Mailing

class Command(BaseCommand):
    help = 'Отправка рассылки'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        mailing = Mailing.objects.get(pk=mailing_id)
        recipients = mailing.recipients.all()

        for recipient in recipients:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email='kovylek.ul@mail.ru',
                recipient_list=[recipient.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена!'))