# Generated by Django 3.2 on 2023-09-13 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0004_alter_facturaproveedor_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefacturaproveedor',
            name='descripcion',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
