# Commande pour réinitialiser les machines (par exemple, dans une nouvelle commande Django)
from django.core.management.base import BaseCommand
from kroschu_application.models import Machine

class Command(BaseCommand):
    help = 'Reset machines to initial state'

    def handle(self, *args, **kwargs):
        machines = Machine.objects.filter(name__in=['US10', 'US11'])
        for machine in machines:
            machine.is_occupied = False
            machine.current_task = None
            machine.task_count = 0
            machine.save()
        self.stdout.write(self.style.SUCCESS('Machines reset successfully'))