# Generated by Django 5.1.6 on 2025-02-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0007_alter_alerte_statut_alter_demande_statut_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=255),
        ),
    ]
