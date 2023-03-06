# Generated by Django 3.2 on 2023-03-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20230306_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='notafiscal',
            name='pontuacao_cliente',
            field=models.IntegerField(default=5, verbose_name='Pontuação do Cliente'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='pontuacao_transportador',
            field=models.IntegerField(default=5, verbose_name='Pontuação do Transportador'),
            preserve_default=False,
        ),
    ]
