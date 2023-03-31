# Generated by Django 3.2 on 2023-03-31 14:24

from django.db import migrations
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20230331_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cnpj',
            field=localflavor.br.models.BRCNPJField(blank=True, max_length=18, null=True, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cpf',
            field=localflavor.br.models.BRCPFField(blank=True, max_length=14, null=True, verbose_name='CPF'),
        ),
        migrations.AddField(
            model_name='transportador',
            name='cnpj',
            field=localflavor.br.models.BRCNPJField(blank=True, max_length=18, null=True, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='transportador',
            name='cpf',
            field=localflavor.br.models.BRCPFField(blank=True, max_length=14, null=True, verbose_name='CPF'),
        ),
    ]
