# Generated by Django 3.2 on 2023-04-04 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_beneficio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontos', models.IntegerField(verbose_name='Pontos gastos')),
                ('data', models.DateField(auto_now_add=True, verbose_name='Data')),
                ('status', models.CharField(choices=[('1', 'Orçamento'), ('2', 'Aprovado'), ('99', 'Cancelado'), ('3', 'Entregue')], default='1', max_length=2, verbose_name='Situação')),
                ('beneficio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.beneficio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-data'],
            },
        ),
    ]
