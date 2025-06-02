from django.core.management.base import BaseCommand
from kroschu_application.models import Tache

class Command(BaseCommand):
    help = 'Reset (delete all) task data'

    def handle(self, *args, **kwargs):
        # Supprimer toutes les données existantes dans la table Tache
        deleted_count = Tache.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} task records'))