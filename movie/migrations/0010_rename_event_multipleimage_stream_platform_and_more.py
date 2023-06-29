# Generated by Django 4.0.4 on 2023-06-29 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_brokerservice_category'),
        ('movie', '0009_streamplatform_created_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multipleimage',
            old_name='event',
            new_name='stream_platform',
        ),
        migrations.RemoveField(
            model_name='streamplatform',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='streamplatform',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stream_platform_subcaterogy', to='services.subcategory'),
        ),
    ]
