
from django.db import models
from model_utils.models import TimeStampedModel

from users.models import Endereco_cliente, User
from produtos.models import *

class Status(models.Model):
    id_status = models.AutoField(unique=True, null=False, primary_key=True)
    Status = models.CharField(max_length=50)
    descricao = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.Status}"

 
    
class Pedido(TimeStampedModel):

    numero_pedido = models.AutoField(unique=True, primary_key=True, null=False)
    id_cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    id_endereco = models.ForeignKey(Endereco_cliente, on_delete=models.CASCADE)
    frete = models.FloatField()
    opcaofrete = models.CharField(max_length=2)
    paid = models.BooleanField(default=False)
    status_pedido = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Pedido{self.numero_pedido}"

    def get_preco_total(self):
        total_cost = sum(item.get_preco_total() for item in self.items.all())
        return total_cost

    def get_description(self):
        return ", ".join(
            [f"{item.qtd} x ({item.id_produto.id_produto}-{item.id_produto.nome})" for item in self.items.all()]

        )    

class ItemPedido(models.Model):

    id_pedido = models.ForeignKey(Pedido, related_name="items", on_delete=models.CASCADE)    

    id_produto = models.ForeignKey(VariacaoProduto, related_name="pedido_items", on_delete=models.CASCADE)

    preco = models.FloatField()

    qtd = models.PositiveIntegerField()

    def get_preco_total(self):
        return self.preco * self.qtd
 

