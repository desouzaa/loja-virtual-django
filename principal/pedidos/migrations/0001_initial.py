# Generated by Django 2.1.15 on 2021-11-23 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produtos', '0015_auto_20211122_1206'),
        ('users', '0007_remove_telefone_cliente_tipo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=15)),
                ('qtd', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('numero_pedido', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('paid', models.BooleanField(default=False)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Endereco_cliente')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='itempedido',
            name='id_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pedidos.Pedido'),
        ),
        migrations.AddField(
            model_name='itempedido',
            name='id_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_items', to='produtos.VariacaoProduto'),
        ),
    ]
