# Generated by Django 5.1.6 on 2025-04-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0046_alertemain_maintenance_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('operateur', 'Opérateur'), ('logistique_incomming', 'Logistique_Incomming'), ('logistique_pagoda', 'Logistique_Pagoda'), ('logistique_kit', 'Logistique_Kit'), ('maintenance_machine', 'Maintenance_Machine'), ('maintenance_board', 'Maintenance_Board'), ('qualite', 'Qualité'), ('chef_equipe', "Chef d'équipe"), ('admin', 'Administrateur')], max_length=50),
        ),
    ]
