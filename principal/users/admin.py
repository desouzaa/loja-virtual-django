from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *
from produtos.models import *

admin.site.register(User, auth_admin.UserAdmin)
admin.site.register(Endereco_cliente)
admin.site.register(Telefone_cliente)
admin.site.register(Produto)
admin.site.register(VariacaoProduto)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Status_Produto)
admin.site.register(Tag)
admin.site.register(Produto_Tag)
admin.site.register(Produto_Material)
admin.site.register(Review)
admin.site.register(Historico_Produto)
admin.site.register(Material)
admin.site.register(Cor)
admin.site.register(Tamanho)
admin.site.register(Estoque)
admin.site.register(Historico_VariacaoProduto)
admin.site.register(fotosProduto)


