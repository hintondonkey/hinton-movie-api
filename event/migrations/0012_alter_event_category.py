# Generated by Django 4.0.4 on 2023-06-23 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_subcategory'),
        ('event', '0011_alter_event_category_delete_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_category', to='services.subcategory'),
        ),
    ]
