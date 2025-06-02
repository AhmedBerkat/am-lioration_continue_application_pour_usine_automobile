import pandas as pd

# Chemin vers le fichier Excel (ajuste selon ton projet)
MACHINE_MAPPING_PATH = r'C:\Users\zoro\Downloads\machine_mapping.xlsx'

def get_compatible_machines(ident_code):
    """
    Retourne la liste des machines compatibles pour un ident_code donné en lisant un fichier Excel.
    Si l'ident_code n'est pas trouvé, retourne une liste vide.
    """
    try:
        # Lire le fichier Excel
        df = pd.read_excel(MACHINE_MAPPING_PATH)
        # Trouver la ligne correspondant à ident_code
        machine_row = df[df['ident_code'] == ident_code]
        if not machine_row.empty:
            # Convertir la chaîne de machines en liste (en supposant qu'elles sont séparées par une virgule)
            machines = str(machine_row['compatible_machines'].iloc[0]).split(', ')
            return [m.strip() for m in machines]
        return []
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel : {e}")
        return []