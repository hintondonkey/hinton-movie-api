# Generated by Django 4.0.4 on 2023-06-19 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('event', '0004_remove_subcategory_broker'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='broker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker_event', to='user_app.broker'),
        ),
    ]