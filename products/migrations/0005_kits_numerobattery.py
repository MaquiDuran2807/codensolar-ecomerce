# Generated by Django 4.1.7 on 2023-03-13 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_kits_description_remove_kits_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kits',
            name='numeroBattery',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]