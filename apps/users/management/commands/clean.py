from django.core.management.base import BaseCommand, CommandError
from apps.web.models import Freebie


class Command(BaseCommand):
    help = 'Resets all users to 0'

    def handle(self, **options):
        Freebie.objects.all().delete()
