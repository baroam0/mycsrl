# Generated by Django 3.2 on 2024-03-14 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alquileres', '0005_auto_20240313_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_inicio', models.IntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')])),
                ('anio_inicio', models.IntegerField(choices=[(2024, 2024)])),
                ('mes_fin', models.IntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')])),
                ('anio_fin', models.IntegerField(choices=[(2024, 2024)])),
                ('finalizado', models.BooleanField()),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alquileres.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='CuotaContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')])),
                ('anio', models.IntegerField(choices=[(2024, 2024)])),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alquileres.contrato')),
            ],
        ),
    ]