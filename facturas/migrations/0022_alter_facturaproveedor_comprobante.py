# Generated by Django 3.2 on 2024-04-26 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0021_remove_detallefacturaproveedor_preciounitario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaproveedor',
            name='comprobante',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
