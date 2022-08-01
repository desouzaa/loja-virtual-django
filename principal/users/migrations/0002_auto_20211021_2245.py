# Generated by Django 2.1.15 on 2021-10-22 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sexo',
            field=models.CharField(choices=[['F', 'Feminino'], ['M', 'Masculino'], ['N', 'Prefiro não informar']], default='n', max_length=1),
        ),
    ]