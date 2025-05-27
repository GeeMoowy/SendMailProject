from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser
from mailings.models import Mailing


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" и назначает необходимые разрешения'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        manager_group, created = Group.objects.get_or_create(name='Менеджеры')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует'))
            return

        permissions = [
            'can_block_user',
            'can_view_all_recipients',
            'can_view_all_mailing',
        ]

        # Находим и добавляем разрешения
        for codename in permissions:
            try:
                # Для кастомных разрешений
                if codename.startswith('can_'):
                    perm = Permission.objects.get(codename=codename)
                else:
                    # Для стандартных разрешений моделей
                    app_label, model = codename.split('_', 1)
                    if model.startswith('mailing'):
                        content_type = ContentType.objects.get_for_model(Mailing)
                    else:
                        content_type = ContentType.objects.get_for_model(CustomUser)

                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )

                manager_group.permissions.add(perm)
                self.stdout.write(self.style.SUCCESS(f'Добавлено разрешение: {codename}'))

            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Разрешение не найдено: {codename}'))

        self.stdout.write(self.style.SUCCESS('Все разрешения успешно добавлены в группу "Менеджеры"'))