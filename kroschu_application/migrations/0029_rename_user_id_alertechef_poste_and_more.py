# Generated by Django 5.1.6 on 2025-03-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0028_user_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alertechef',
            old_name='user_id',
            new_name='poste',
        ),
        migrations.RenameField(
            model_name='alertemain',
            old_name='user_id',
            new_name='poste',
        ),
        migrations.RenameField(
            model_name='alertequal',
            old_name='user_id',
            new_name='poste',
        ),
        migrations.RenameField(
            model_name='demande',
            old_name='user_id',
            new_name='poste',
        ),
        migrations.RenameField(
            model_name='tache',
            old_name='user_id',
            new_name='poste',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nom_prenom',
        ),
        migrations.RemoveField(
            model_name='user',
            name='shift',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='poste',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
