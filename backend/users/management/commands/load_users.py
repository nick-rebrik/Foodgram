import json

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create test users'

    def handle(self, *args, **options):
        with open('data/users.json', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                user, created = User.objects.get_or_create(
                    username=item['username'],
                    email=item['email'],
                    first_name=item['first_name'],
                    last_name=item['last_name']
                )
                user.set_password(item['password'])
                user.save()
