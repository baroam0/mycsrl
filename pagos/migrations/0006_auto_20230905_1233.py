# Generated by Django 3.2 on 2023-09-05 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bancos', '0001_initial'),
        ('pagos', '0005_ordenpago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenpago',
            name='banco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bancos.banco'),
        ),
        migrations.AlterField(
            model_name='ordenpago',
            name='fechacheque',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='ordenpago',
            name='modopago',
            field=models.CharField(choices=[('Cheque', 'Cheque'), ('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia')], default='Unidad', max_length=20),
        ),
        migrations.AlterField(
            model_name='ordenpago',
            name='numerocheque',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]