# Generated by Django 5.1.6 on 2025-03-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroschu_application', '0031_user_is_active_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
