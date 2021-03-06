import datetime
import urllib

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from apps.profiles.models import User


class Command(BaseCommand):
    help = 'Tries to verify gravatar for recently joined users.'

    def handle(self, *args, **options):
        users_verified = []
        users_not_verified = []
        users = User.objects.filter(
            date_joined__gte=now() - datetime.timedelta(hours=24))

        for user in users:
            try:
                urllib.request.urlopen(user.gravatar_url)
                user.is_gravatar_verified = True
                user.save()
                users_verified.append(user)
            except urllib.error.HTTPError:
                users_not_verified.append(user)

        self.stdout.write('Verified {} users.\nUnverifed {} users.'.format(
            len(users_verified), len(users_not_verified)))
