# Generated by Django 4.0.4 on 2023-06-23 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0002_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='broker',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='created_user',
        ),
    ]
