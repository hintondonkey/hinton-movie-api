# Generated by Django 4.0.4 on 2023-04-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_streamplatform_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamplatform',
            name='active_noti',
            field=models.BooleanField(default=False),
        ),
    ]
