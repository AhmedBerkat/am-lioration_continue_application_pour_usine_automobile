from django.core.management.base import BaseCommand
from kroschu_application.models import Machine, User

class Command(BaseCommand):
    help = 'Assign all machines to their corresponding postes'

    def handle(self, *args, **kwargs):
        # Mapping complet machine -> poste
        machine_poste_mapping = {
            'US10': '10',
            'US11': '11',
            'US12': '12',
            'US15': '15',
            'US19': '19',
            'US43': '43',
            'US17': '17',
            'US8': '8',
            # Ajoutez toutes les autres machines
        }

        for machine_name, poste_name in machine_poste_mapping.items():
            try:
                machine = Machine.objects.get(name=machine_name)
                poste = User.objects.get(poste=poste_name, role='operateur')
                machine.poste = poste
                machine.save()
                self.stdout.write(self.style.SUCCESS(f'Assigned {machine_name} to Poste {poste_name}'))
            except Machine.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Machine {machine_name} not found'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Poste {poste_name} with role operateur not found'))

        self.stdout.write(self.style.SUCCESS('Finished assigning all machines to postes'))