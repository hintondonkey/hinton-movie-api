# Generated by Django 4.0.4 on 2023-06-20 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_rename_sbroker_subcategory_broker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='user',
            new_name='created_user',
        ),
    ]
