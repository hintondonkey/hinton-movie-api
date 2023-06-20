# Generated by Django 4.0.4 on 2023-06-20 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('event', '0006_rename_user_event_created_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='sbroker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker_subcategory', to='user_app.broker'),
        ),
    ]
