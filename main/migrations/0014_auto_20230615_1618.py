# Generated by Django 3.2 on 2023-06-15 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_pedido_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracaopontuacao',
            name='reais_por_ponto',
        ),
        migrations.RemoveField(
            model_name='notafiscal',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='notafiscal',
            name='item',
        ),
        migrations.RemoveField(
            model_name='notafiscal',
            name='valor',
        ),
        migrations.AddField(
            model_name='configuracaopontuacao',
            name='toneladas_por_ponto',
            field=models.IntegerField(default=100, help_text='Quantos toneladas serão necessários para gerar 1 ponto pro cliente.', verbose_name='Toneladas por Ponto'),
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='produto',
            field=models.CharField(choices=[('Brita 1', 'Brita 1'), ('Brita 0', 'Brita 0'), ('Po de pedra', 'Po de pedra'), ('Brita corrida', 'Brita corrida'), ('BGS', 'BGS'), ('Brita 1/2', 'Brita 1/2'), ('Pedra rachão', 'Pedra rachão')], default='', max_length=100, verbose_name='Produto'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='toneladas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13, verbose_name='Toneladas'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('1', 'Pendente'), ('2', 'Aprovado'), ('99', 'Cancelado'), ('3', 'Entregue')], default='1', max_length=2, verbose_name='Situação'),
        ),
    ]