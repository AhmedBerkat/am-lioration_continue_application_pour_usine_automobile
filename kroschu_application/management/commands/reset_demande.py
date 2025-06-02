from django.core.management.base import BaseCommand
from kroschu_application.models import Demande

class Command(BaseCommand):
    help = 'Reset Demande records to initial state'

    def handle(self, *args, **kwargs):
        # Fetch all Demande records
        demandes = Demande.objects.all()

        # Check if there are any records to reset
        if not demandes.exists():
            self.stdout.write(self.style.WARNING('No Demande records found to reset.'))
            return

        # Reset each Demande record
        count = 0
        for demande in demandes:
            demande.statut = 'en_attente'
            demande.wires.clear()  # Clear the ManyToMany relationship with wires
            demande.validated_at = None
            demande.save()
            count += 1

        # Output success message
        self.stdout.write(self.style.SUCCESS(f'Successfully reset {count} Demande records.'))