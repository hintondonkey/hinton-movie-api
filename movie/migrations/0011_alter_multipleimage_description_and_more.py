# Generated by Django 4.0.4 on 2023-07-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0010_rename_event_multipleimage_stream_platform_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multipleimage',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='multipleimage',
            name='file_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='multipleimage',
            name='file_size',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='multipleimage',
            name='name',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
