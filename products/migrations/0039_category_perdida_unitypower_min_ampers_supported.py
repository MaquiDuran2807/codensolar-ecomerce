# Generated by Django 4.2 on 2023-05-07 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_unitypower_battery_kids_supported_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='perdida',
            field=models.FloatField(blank=True, default=39, null=True),
        ),
        migrations.AddField(
            model_name='unitypower',
            name='min_ampers_supported',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]