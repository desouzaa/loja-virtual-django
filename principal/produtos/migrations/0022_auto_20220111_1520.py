# Generated by Django 3.2.9 on 2022-01-11 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0021_alter_review_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotosproduto',
            name='foto',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='produto',
            name='fotoPr',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variacaoproduto',
            name='foto',
            field=models.TextField(),
        ),
    ]
