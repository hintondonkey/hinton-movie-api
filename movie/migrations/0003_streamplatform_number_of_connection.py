# Generated by Django 4.0.4 on 2023-06-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_rename_subcaterogy_subcategory_delete_caterogy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamplatform',
            name='number_of_connection',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]