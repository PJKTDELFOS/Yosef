# Generated by Django 5.1.2 on 2024-11-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0007_alter_processo_modalidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratos',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]