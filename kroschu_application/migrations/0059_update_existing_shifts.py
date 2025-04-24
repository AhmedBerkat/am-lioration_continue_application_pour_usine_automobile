from django.db import migrations
from django.utils.timezone import localtime
from datetime import datetime

def update_shifts(apps, schema_editor):
    models_to_update = ['Demande', 'Alertemain', 'Alertequal', 'Alertechef', 'Tache']
    
    for model_name in models_to_update:
        Model = apps.get_model('kroschu_application', model_name)
        for obj in Model.objects.all():
            hour = localtime(obj.created_at).hour
            if 22 <= hour or hour < 6:
                obj.shift = 'A'
            elif 6 <= hour < 14:
                obj.shift = 'B'
            else:
                obj.shift = 'C'
            obj.save(update_fields=['shift'])

class Migration(migrations.Migration):
    dependencies = [
        ('kroschu_application', '0058_alter_alertechef_shift_alter_alertemain_shift_and_more'),
    ]

    operations = [
        migrations.RunPython(update_shifts, reverse_code=migrations.RunPython.noop),
    ]