# Generated by Django 4.0.4 on 2023-07-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_alter_multipleimage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamplatform',
            name='sub_icon',
            field=models.TextField(blank=True, null=True),
        ),
    ]
