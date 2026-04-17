import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Створює суперюзера з env vars: DJANGO_SUPERUSER_USERNAME '
        '(або DJANGO_SUPERUSER_NAME), DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD'
    )

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME') or os.environ.get(
            'DJANGO_SUPERUSER_NAME'
        )
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write('  create_admin: env vars не задані, пропускаємо.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'  create_admin: користувач "{username}" вже існує.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'  Суперюзер "{username}" створений.'))
