# Generated by Django 4.0.4 on 2023-07-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_alter_broker_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]