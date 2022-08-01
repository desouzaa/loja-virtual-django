from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField


class User(AbstractUser):

    SEXO_CHOICES = [
        ["F", "Feminino"],
        ["M", "Masculino"],
        ["N", "Prefiro não informar"]
    ]

        
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='n')
    datanascimento = models.CharField(max_length=11)
    cpf = models.CharField(max_length=11)
      
class Telefone_cliente(models.Model):


    TEL_CHOICES = [
        ["P", "Principal"],
        ["S", "Secundario"],
    ]

    id_telefone = models.AutoField(primary_key=True, null=False, unique=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)  

class Endereco_cliente(models.Model):

    id_endereco = models.AutoField(primary_key=True, null=False, unique=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.CharField(max_length=11)
    bairro = models.CharField(max_length=50)
    estado = CharField(max_length=30)
    complemento1 = CharField(max_length=50)
    complemento2 = CharField(max_length=50)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)  


