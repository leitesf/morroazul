# Generated by Django 3.2 on 2023-11-30 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20231121_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracaopontuacao',
            name='kms_por_ponto',
        ),
        migrations.RemoveField(
            model_name='notafiscal',
            name='pontuacao_transportador',
        ),
    ]
