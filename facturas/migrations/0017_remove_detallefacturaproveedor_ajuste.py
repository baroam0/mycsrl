# Generated by Django 3.2 on 2023-09-27 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0016_auto_20230927_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallefacturaproveedor',
            name='ajuste',
        ),
    ]
