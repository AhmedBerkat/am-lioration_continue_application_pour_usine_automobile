# Generated by Django 5.1.6 on 2025-04-23 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0049_alter_demande_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertechef',
            name='shift',
            field=models.CharField(default='A', editable=False, max_length=1),
        ),
        migrations.AlterField(
            model_name='alertemain',
            name='shift',
            field=models.CharField(default='A', editable=False, max_length=1),
        ),
        migrations.AlterField(
            model_name='alertequal',
            name='shift',
            field=models.CharField(default='A', editable=False, max_length=1),
        ),
    ]
