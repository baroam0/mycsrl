# Generated by Django 3.2 on 2023-09-17 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0007_rename_descripcion_detallefacturaproveedor_descripciondetalle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='descripciondetalle',
            options={'verbose_name_plural': 'Descripcion Detalle'},
        ),
    ]