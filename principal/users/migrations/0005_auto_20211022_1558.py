# Generated by Django 2.1.15 on 2021-10-22 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211022_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='endereco_cliente',
            name='complememento2',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endereco_cliente',
            name='complemento1',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
    ]
