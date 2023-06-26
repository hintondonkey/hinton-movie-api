# Generated by Django 4.0.4 on 2023-06-25 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_subcategory_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brokerservice',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brokerservice',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
