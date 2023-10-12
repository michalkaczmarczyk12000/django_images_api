from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Tier


class Command(BaseCommand):
    help = 'deletes expired events'

    def handle(self, *args, **options):
        self.stdout.write('Expired events successfully deleted.')


basic = get_user_model().objects.create_user(
            username='user_basic',
            email='basic@mail.com',
            password='user_basic',
            is_staff=True,
            is_active=True,
            user_tier=Tier.objects.get(id=1)
        )
basic.save()
premium = get_user_model().objects.create_user(
            username='user_premium',
            email='premium@mail.com',
            password='user_premium',
            is_staff=True,
            is_active=True,
            user_tier=Tier.objects.get(id=2)
        )
premium.save()
enterprise = get_user_model().objects.create_user(
            username='user_enterprise',
            email='enterprise@mail.com',
            password='user_enterprise',
            is_staff=True,
            is_active=True,
            user_tier=Tier.objects.get(id=3)
        )
enterprise.save()

get_user_model().objects.create_superuser('admin', 'admin@admin', 'admin')
