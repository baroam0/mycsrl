# Generated by Django 3.2 on 2024-03-16 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquileres', '0008_auto_20240315_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='anio_fin',
            field=models.IntegerField(choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='anio_inicio',
            field=models.IntegerField(choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='finalizado',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cuotacontrato',
            name='anio',
            field=models.IntegerField(choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='anio',
            field=models.IntegerField(choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
    ]
