# Generated by Django 3.2.9 on 2021-12-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20211215_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='desconto',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
