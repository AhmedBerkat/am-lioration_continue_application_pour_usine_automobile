# Generated by Django 5.1.6 on 2025-03-12 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0024_rename_nom_user_nom_prenom_rename_prenom_user_poste_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='description',
        ),
        migrations.RemoveField(
            model_name='demande',
            name='type_materiel',
        ),
    ]
