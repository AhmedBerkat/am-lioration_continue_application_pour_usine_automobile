# Generated by Django 5.1.6 on 2025-04-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0044_demande_logistique_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='logistique_type',
            field=models.CharField(blank=True, choices=[('logistique_incomming', 'Logistique Incomming'), ('logistique_pagoda', 'Logistique Pagoda'), ('logistique_kit', 'Logistique Kit')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('operateur', 'Opérateur'), ('logistique_incomming', 'Logistique_Incomming'), ('logistique_pagoda', 'Logistique_Pagoda'), ('logistique_kit', 'Logistique_Kit'), ('maintenance', 'Maintenance'), ('qualite', 'Qualité'), ('chef_equipe', "Chef d'équipe"), ('admin', 'Administrateur')], max_length=50),
        ),
    ]
