
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from account.models import User

class Command(BaseCommand):
    help = 'Delete users who have been inactive (is_active=False) for more than 10 minutes since creation'

    def handle(self, *args, **kwargs):
        cutoff_time = timezone.now() - timedelta(minutes=10)

        users_to_delete = User.objects.filter(
            is_active=False,
            created_at__lte=cutoff_time
        )

        count = users_to_delete.count()
        
        users_to_delete.delete()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} inactive users that were created more than 10 minutes ago')
        )