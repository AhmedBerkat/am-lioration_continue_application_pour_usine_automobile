from django.core.management.base import BaseCommand
from kroschu_application.models import Wire
import pandas as pd

class Command(BaseCommand):
    help = 'Populate wire data from an Excel file'

    def handle(self, *args, **kwargs):
        # Chemin vers le fichier Excel (corrigé pour Windows)
        WIRES_DATA_PATH = r'C:\Users\zoro\Downloads\wires_data.xlsx'

        try:
            # Lire le fichier Excel
            df = pd.read_excel(WIRES_DATA_PATH)
            # Créer les objets Wire (pas de get_or_create pour permettre les doublons)
            for index, row in df.iterrows():
                wire_data = {
                    'ident_code': row['ident_code'],
                    'section': row['section'],
                    'length': row['length'],
                    'color': row['color'],
                    'position': row['position'],
                    'L_ident': row['L_ident'],
                    'version': row['version']
                }
                Wire.objects.create(**wire_data)
            self.stdout.write(self.style.SUCCESS('Successfully populated wire data from Excel'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error populating wire data: {e}'))