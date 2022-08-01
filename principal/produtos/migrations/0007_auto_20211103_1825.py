# Generated by Django 2.1.15 on 2021-11-03 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0006_review_id_produto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cor',
            fields=[
                ('id_cor', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=20)),
                ('fotoCor', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Historico_VariacaoProduto',
            fields=[
                ('id_historico', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tamanho',
            fields=[
                ('id_tamanho', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='VariacaoProduto',
            fields=[
                ('id_variacao', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('preco', models.FloatField()),
                ('id_cor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.Cor')),
                ('id_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.Produto')),
                ('id_status_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.Status_Produto')),
                ('id_tamanho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.Tamanho')),
            ],
        ),
        migrations.AddField(
            model_name='historico_variacaoproduto',
            name='id_VariacaoProduto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.VariacaoProduto'),
        ),
        migrations.AddField(
            model_name='estoque',
            name='id_variacaoProduto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.VariacaoProduto'),
        ),
    ]