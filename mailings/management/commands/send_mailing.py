from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from ...models import Mailing, SendingAttempt


class Command(BaseCommand):
    help = 'Send mailing to all recipients'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID of the mailing to send')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Mailing with ID {mailing_id} does not exist'))
            return

        recipients = mailing.recipients.all()
        total_recipients = recipients.count()
        success_count = 0
        error_count = 0

        self.stdout.write(
            self.style.SUCCESS(f'Starting mailing "{mailing.message.subject}" to {total_recipients} recipients'))

        for recipient in recipients:
            attempt = SendingAttempt(mailing=mailing)

            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email='kovylek.ul@mail.ru',
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                attempt.status = 'Успешно'
                attempt.response = 'Письмо успешно отправлено.'
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully sent to {recipient.email}'))

            except Exception as e:
                attempt.status = 'Не успешно'
                attempt.response = str(e)
                error_count += 1
                self.stdout.write(self.style.ERROR(f'Error sending to {recipient.email}: {str(e)}'))

            attempt.save()

        self.stdout.write(self.style.SUCCESS(
            f'Mailing completed! Success: {success_count}, Errors: {error_count}, Total: {total_recipients}'
        ))