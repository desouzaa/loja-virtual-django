# Generated by Django 3.2.9 on 2021-12-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0019_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='titulo',
            field=models.CharField(max_length=40),
        ),
    ]