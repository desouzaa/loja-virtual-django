# Generated by Django 2.1.15 on 2021-11-03 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_auto_20211103_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='id_produto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='produtos.Produto'),
            preserve_default=False,
        ),
    ]
