# Generated by Django 4.2 on 2023-04-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_breakers_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battery',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/Battery'),
        ),
        migrations.AlterField(
            model_name='breakers',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/breakers'),
        ),
        migrations.AlterField(
            model_name='inversores',
            name='image',
            field=models.ImageField(upload_to='media/Inversores'),
        ),
        migrations.AlterField(
            model_name='otros',
            name='image',
            field=models.ImageField(upload_to='media/otros'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(upload_to='media/Otros'),
        ),
        migrations.AlterField(
            model_name='reguladores',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/Reguladores'),
        ),
        migrations.AlterField(
            model_name='solarpanel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/SolarPanel'),
        ),
        migrations.AlterField(
            model_name='soportes',
            name='image',
            field=models.ImageField(upload_to='media/soportes'),
        ),
        migrations.AlterField(
            model_name='unidadpotencia',
            name='image',
            field=models.ImageField(upload_to='media/UnidadPotencia'),
        ),
    ]