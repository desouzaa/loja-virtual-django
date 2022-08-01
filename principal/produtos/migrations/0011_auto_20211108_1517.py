# Generated by Django 2.1.15 on 2021-11-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0010_auto_20211108_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='foto2',
            field=models.ImageField(blank=True, null=True, upload_to='produtos'),
        ),
        migrations.AddField(
            model_name='produto',
            name='foto3',
            field=models.ImageField(blank=True, null=True, upload_to='produtos'),
        ),
        migrations.AddField(
            model_name='produto',
            name='foto4',
            field=models.ImageField(blank=True, null=True, upload_to='produtos'),
        ),
        migrations.AlterField(
            model_name='cor',
            name='fotoCor',
            field=models.ImageField(upload_to='cores'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='foto',
            field=models.ImageField(upload_to='produtos'),
        ),
        migrations.AlterField(
            model_name='variacaoproduto',
            name='foto',
            field=models.ImageField(upload_to='variacoes'),
        ),
    ]