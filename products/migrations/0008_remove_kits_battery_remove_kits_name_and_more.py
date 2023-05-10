# Generated by Django 4.1.7 on 2023-03-30 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_battery_voltage_products_voltage_solarpanel_voltage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kits',
            name='battery',
        ),
        migrations.RemoveField(
            model_name='kits',
            name='name',
        ),
        migrations.RemoveField(
            model_name='kits',
            name='numeroBattery',
        ),
        migrations.RemoveField(
            model_name='kits',
            name='otros',
        ),
        migrations.RemoveField(
            model_name='kits',
            name='panels',
        ),
        migrations.RemoveField(
            model_name='kits',
            name='reguladores',
        ),
        migrations.AddField(
            model_name='kits',
            name='panel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.solarpanel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kits',
            name='panelAmount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
