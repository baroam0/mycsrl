# Generated by Django 3.2 on 2024-01-27 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='domicilio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]