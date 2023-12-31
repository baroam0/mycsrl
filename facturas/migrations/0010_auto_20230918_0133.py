# Generated by Django 3.2 on 2023-09-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0009_detallefacturaproveedor_ajuste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallefacturaproveedor',
            name='descuento',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='detallefacturaproveedor',
            name='descuentoporcentaje',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20),
        ),
    ]
