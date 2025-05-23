# Generated by Django 5.1.6 on 2025-04-23 15:59

import kroschu_application.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0052_remove_alertechef_shift_remove_alertemain_shift_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertechef',
            name='shift',
            field=models.CharField(default=kroschu_application.models.determine_shift, max_length=1),
        ),
        migrations.AddField(
            model_name='alertemain',
            name='shift',
            field=models.CharField(default=kroschu_application.models.determine_shift, max_length=1),
        ),
        migrations.AddField(
            model_name='alertequal',
            name='shift',
            field=models.CharField(default=kroschu_application.models.determine_shift, max_length=1),
        ),
        migrations.AddField(
            model_name='demande',
            name='shift',
            field=models.CharField(default=kroschu_application.models.determine_shift, max_length=1),
        ),
        migrations.AddField(
            model_name='tache',
            name='shift',
            field=models.CharField(default=kroschu_application.models.determine_shift, max_length=1),
        ),
    ]
