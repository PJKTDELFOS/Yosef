# Generated by Django 5.1.2 on 2024-11-25 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0013_alter_processo_modalidade_alter_processo_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processo',
            name='data_disputa',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]