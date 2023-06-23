# Generated by Django 4.0.4 on 2023-06-23 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0002_subcategory'),
        ('movie', '0003_streamplatform_number_of_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamplatform',
            name='approval',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='streamplatform',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stream_platform_caterogy', to='lookup.category'),
        ),
        migrations.AddField(
            model_name='streamplatform',
            name='is_horizontal',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='streamplatform',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='streamplatform',
            name='subcategory',
            field=models.ManyToManyField(null=True, related_name='stream_platform_subcaterogy', to='lookup.subcategory'),
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]