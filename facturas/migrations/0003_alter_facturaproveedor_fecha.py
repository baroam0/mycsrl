# Generated by Django 3.2 on 2023-09-12 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0002_auto_20230911_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaproveedor',
            name='fecha',
            field=models.DateField(null=True),
        ),
    ]