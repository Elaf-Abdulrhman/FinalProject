# Generated by Django 5.2 on 2025-04-27 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_athlete_profilephoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]
