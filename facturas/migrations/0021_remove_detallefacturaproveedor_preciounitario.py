# Generated by Django 3.2 on 2023-12-20 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0020_detallefacturaproveedor_preciototal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallefacturaproveedor',
            name='preciounitario',
        ),
    ]
