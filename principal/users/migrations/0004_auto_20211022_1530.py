# Generated by Django 2.1.15 on 2021-10-22 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_endereco_cliente_telefone_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco_cliente',
            name='bairro',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='endereco_cliente',
            name='cep',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='endereco_cliente',
            name='cidade',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='endereco_cliente',
            name='estado',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='endereco_cliente',
            name='rua',
            field=models.CharField(max_length=50),
        ),
    ]
