# Generated by Django 5.1.2 on 2024-11-25 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0009_contratos_apolice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processo',
            name='data_disputa',
            field=models.DateTimeField(blank=True),
        ),
    ]