# Generated by Django 4.1.7 on 2023-03-03 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='codregistro',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]