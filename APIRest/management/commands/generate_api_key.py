from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import APIKey
import uuid

#superusuario 4864065c4f4f4646b2f9a80519cdfe86
#analyst      b577f193a72d41de88d98f14f52015e1

class Command(BaseCommand):
    help = 'Generate an API Key for a user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID of the user to generate API Key for')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
            return

        new_key = uuid.uuid4().hex
        api_key = APIKey(key=new_key, user=user)
        api_key.save()

        self.stdout.write(self.style.SUCCESS(f'API Key generated for user {user.username}: {new_key}'))
