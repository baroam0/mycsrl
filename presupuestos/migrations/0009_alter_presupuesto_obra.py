# Generated by Django 3.2 on 2024-09-06 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0016_obra_finalizada'),
        ('presupuestos', '0008_auto_20240820_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='obra',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pagos.obra'),
        ),
    ]