# Generated by Django 3.2 on 2023-09-23 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='fechabaja',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personal',
            name='fechaingreso',
            field=models.DateField(blank=True, null=True),
        ),
    ]
