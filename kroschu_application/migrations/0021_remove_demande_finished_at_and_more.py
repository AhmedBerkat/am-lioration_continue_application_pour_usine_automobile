# Generated by Django 5.1.6 on 2025-03-07 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0020_rename_date_traitement_demande_finished_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='finished_at',
        ),
        migrations.RemoveField(
            model_name='demande',
            name='temps_ecoule',
        ),
    ]
