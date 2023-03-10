# Generated by Django 3.2 on 2023-03-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20230306_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoPontuacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kms_por_ponto', models.IntegerField(default=100, help_text='Quantos KM serão necessários para gerar 1 ponto pro transportador.', verbose_name='KMs por Ponto')),
                ('reais_por_ponto', models.IntegerField(default=100, help_text='Quantos reais serão necessários para gerar 1 ponto pro cliente.', verbose_name='Reais por Ponto')),
            ],
            options={
                'verbose_name': 'Configuração de Pontos',
            },
        ),
    ]
