# Generated by Django 5.1.2 on 2024-12-03 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='data_hora_att',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='local_entrega',
            field=models.TextField(blank=True, default='', max_length=350),
        ),
    ]