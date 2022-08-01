from django.db import models
from produtos.models import Produto, VariacaoProduto
from users.models import User
from pedidos.models import Pedido

class Tipo_solicitacao(models.Model):
    id_tipo = models.AutoField(primary_key=True, null=False, unique=True)
    descricao = models.CharField(max_length=100)
    
class Status_solicitacao(models.Model):
     id_status = models.AutoField(primary_key=True, null=False, unique=True)
     descricao = models.CharField(max_length=100)

class Solicitacoes(models.Model):

    id_solicitacao = models.AutoField(primary_key=True, null=False, unique=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    pedidoSolicitacao = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo_solicitacao, on_delete=models.CASCADE)    
    status = models.ForeignKey(Status_solicitacao, on_delete=models.CASCADE)
    descricao = models.TextField()

class Cupons(models.Model):
    cupom = models.CharField(primary_key=True, null=False, unique=True, max_length=20)    
    desconto = models.IntegerField()
    max = models.IntegerField()

class Cupon_cliente(models.Model):
    cupom = models.ForeignKey(Cupons, on_delete=models.CASCADE) 
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

class Favoritos(models.Model):

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)   

class Newsletter(models.Model):

    email = models.EmailField(unique=True, null=False)    

