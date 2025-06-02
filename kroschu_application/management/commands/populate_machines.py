from django.core.management.base import BaseCommand
from kroschu_application.models import Machine

class Command(BaseCommand):
    help = 'Populate sample machine data'

    def handle(self, *args, **kwargs):
        machines = [
            {'name': 'US10'},
            {'name': 'US11'},
            {'name': 'US12'},
            {'name': 'US15'},
        ]
        for machine in machines:
            Machine.objects.get_or_create(**machine)
        self.stdout.write(self.style.SUCCESS('Successfully populated machine data'))