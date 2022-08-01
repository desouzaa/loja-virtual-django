from django.db import models
from users.models import User
 
class Marca(models.Model):

    id_marca = models.AutoField(primary_key=True, null=False, unique=True)
    nome = models.CharField(max_length=20, null=False)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
   
class Categoria(models.Model):

    id_categoria = models.AutoField(primary_key=True, null=False, unique=True)
    nome = models.CharField(max_length=20, null=False)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
class Subcategoria(models.Model):

    id_subcategoria = models.AutoField(primary_key=True, null=False, unique=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=20, null=False)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
class Status_Produto(models.Model):

    id_status_produto = models.AutoField(primary_key=True, null=False, unique=True)
    descricao = models.CharField(max_length=20, null=False)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao
   
class Tag(models.Model):

    id_tag = models.AutoField(primary_key=True, null=False, unique=True)
    tag = models.CharField(max_length=20, null=False)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag
     
class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True, null=False, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    id_subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    id_status = models.ForeignKey(Status_Produto, on_delete=models.CASCADE)
    estoque_min = models.IntegerField()
    estoque_max = models.IntegerField()
    informacao_tec = models.TextField()
    
    
    
    
    def __str__(self):
        return f'{self.id_produto} ({self.nome})'
    
class Produto_Tag(models.Model):

    id_tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    id_produto = models.ForeignKey(Produto,on_delete=models.CASCADE)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f'{self.id_produto}-{self.id_tag}')
         
class Material(models.Model):

    id_material = models.AutoField(primary_key=True, null=False, unique=True)
    descricao = models.CharField(max_length=30)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.descricao

class Produto_Material(models.Model):

    id_produto = models.ForeignKey(Produto,on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material,on_delete=models.CASCADE)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return str(f'{self.id_produto}-{self.id_material}')

class Review(models.Model):

    id_review = models.AutoField(primary_key=True, null=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=5)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=40)
    descricao = models.TextField(max_length=1000)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return str(f'{self.id_review}--{self.id_produto}--{self.titulo}')

class Historico_Produto(models.Model):

    id_historico = models.AutoField(primary_key=True, null=False, unique=True)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    descricao = models.TextField()
    
    def __str__(self):
        return self.id_historico

class Cor(models.Model):

    id_cor = models.AutoField(primary_key=True, null=False, unique=True)
    nome = models.CharField(max_length=20)
    fotoCor = models.ImageField(upload_to='cores')

    def __str__(self):
        return self.nome

class Tamanho(models.Model):

    id_tamanho = models.AutoField(primary_key=True, null=False, unique=True)
    descricao = models.CharField(max_length=15)

    def __str__(self):
        return self.descricao

class VariacaoProduto(models.Model):


    id_variacao = models.AutoField(primary_key=True, null=False, unique=True)   
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    id_cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    id_tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    id_status_produto = models.ForeignKey(Status_Produto, on_delete=models.CASCADE)
    foto = models.ImageField()
    

    def __str__(self):
        return str(f'{self.id_variacao} -- {self.id_produto} -- {self.id_cor} -- {self.id_tamanho}')

class Estoque(models.Model):

    id_variacaoProduto = models.OneToOneField(VariacaoProduto, on_delete=models.CASCADE) 
    qtd = models.IntegerField() 

    def __str__(self):
        return str(f'{self.id_variacaoProduto} -- {self.qtd}unidades')
        
class Historico_VariacaoProduto(models.Model):

    id_historico = models.AutoField(primary_key=True, null=False, unique=True)
    id_VariacaoProduto = models.ForeignKey(VariacaoProduto, on_delete=models.CASCADE)
    descricao = models.TextField()
    
    def __str__(self):
        return self.id_historico    

class fotosProduto(models.Model):

    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)         
    foto = models.ImageField()