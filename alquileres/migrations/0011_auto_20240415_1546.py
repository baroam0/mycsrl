# Generated by Django 3.2 on 2024-04-15 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquileres', '0010_alter_contrato_finalizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='anio_fin',
            field=models.IntegerField(choices=[(0, '---------'), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='anio_inicio',
            field=models.IntegerField(choices=[(0, '---------'), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='mes_fin',
            field=models.IntegerField(choices=[(0, '------'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')]),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='mes_inicio',
            field=models.IntegerField(choices=[(0, '------'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')]),
        ),
        migrations.AlterField(
            model_name='cuotacontrato',
            name='anio',
            field=models.IntegerField(choices=[(0, '---------'), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='cuotacontrato',
            name='mes',
            field=models.IntegerField(choices=[(0, '------'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')]),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='anio',
            field=models.IntegerField(choices=[(0, '---------'), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034)]),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='mes',
            field=models.IntegerField(choices=[(0, '------'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')]),
        ),
    ]
