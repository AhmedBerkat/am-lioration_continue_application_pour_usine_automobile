# Generated by Django 5.1.6 on 2025-03-19 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('kroschu_application', '0037_customuser_alter_demande_poste_alter_tache_poste_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='User',
        ),
    ]
