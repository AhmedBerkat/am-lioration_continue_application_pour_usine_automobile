from django.core.management.base import BaseCommand
from kroschu_application.models import Wire

class Command(BaseCommand):
    help = 'Reset (delete all) wire data'

    def handle(self, *args, **kwargs):
        # Supprimer toutes les données existantes dans la table Wire
        deleted_count = Wire.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} wire records'))