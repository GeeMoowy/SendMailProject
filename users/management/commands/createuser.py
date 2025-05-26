from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает обычного пользователя с указанными email и паролем'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя')
        parser.add_argument('password', type=str, help='Пароль пользователя')

    def handle(self, *args, **options):
        try:
            user = User.objects.create_user(
                email=options['email'],
                username=options['email'],  # Используем email как username
                password=options['password']
            )
            self.stdout.write(
                self.style.SUCCESS(f'Пользователь {user.email} успешно создан!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {str(e)}')
            )