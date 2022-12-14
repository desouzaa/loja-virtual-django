# Generated by Django 3.2.9 on 2021-11-30 02:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedidos', '0004_auto_20211125_2128'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupons',
            fields=[
                ('cupom', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('desconto', models.IntegerField()),
                ('max', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Status_solicitacao',
            fields=[
                ('id_status', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_solicitacao',
            fields=[
                ('id_tipo', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitacoes',
            fields=[
                ('id_solicitacao', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.TextField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pedidoSolicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outros.status_solicitacao')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outros.tipo_solicitacao')),
            ],
        ),
    ]
