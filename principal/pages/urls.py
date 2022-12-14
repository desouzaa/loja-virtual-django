from os import name
from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.vazio),
    path('index.html', views.index, name='index'),
    path('products/<str:categoria>', views.products, name='products'),
    path('account.html/', views.account, name='account'),
    path('enderecos.html/', views.enderecos, name='enderecos'),
    path('telefones.html/', views.telefones, name="telefones"),
    path('contact.html/', views.contact, name='contact'),
    path('login.html/', views.login, name='login'),
    path('single.html/<int:id>', views.single, name='single'),
    path('checkout.html/', views.checkout, name='checkout'),
    path('cadastrarCliente/', views.cadastarCliente, name ='cadastarCliente'),
    path('logarCliente/', views.logarCliente, name='logarCliente'),
    path('logout/', views.sair, name='logout'),
    path('alterarFrm.html/', views.alterarFrm, name="alterarFrm" ),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('meusdados.html/', views.meusdados, name='meusdados'),
    path('cadastrarEndereco/', views.cadastrarEndereco, name='cadastrarEndereco'),
    path('cadastrarTelefone/', views.cadastrarTelefone, name='cadastrarTelefone'),
    path('excluirTelefone/<int:id>/', views.excluirTelefone, name="excluirTelefone"),
    path('editarTelefone/<int:id>/', views.editarTelefone, name="editarTelefone"),
    path('accounts/login/', views.login),
    path('excluirEndereco/<int:id>/', views.excluirEndereco, name='excluirEndereco'),
    path('excluirEndereco2/<int:id>/', views.excluirEndereco2, name='excluirEndereco2'),
    path('editarEndereco/<int:id>/', views.editarEndereco, name='editarEndereco'),
    path('editarDados/', views.editarDados, name='editarDados'),
    path('salvarDadosEditados/', views.salvarDadosEditados, name="salvarDadosEditados"),
    path('salvarEnderecoEditado/<int:id>', views.salvarEnderecoEditado, name='salvarEnderecoEditado'),
    path('salvarTelefoneEditado/<int:id>', views.salvarTelefoneEditado, name='salvarTelefoneEditado'),
    path('buscarProduto/', views.buscarProduto, name='buscarProduto'),
    path('resetPassword1.html/', views.resetPassword1, name='resetPassword1'),
    path('resetPassword2/', views.resetPassword2, name='resetPassword2'),
    path('carrinho.html/', views.carrinho, name='carrinho'),
    path('calcular', views.calcular, name='calcular'),
    path('consultarEstoque', views.consultarEstoque, name='consultarEstoque'),
    path('finalizarPedido/', views.finalizarPedido, name='finalizarPedido'),
    path('meusPedidos/', views.meusPedidos, name='meusPedidos'),
    path('pedido/<int:id>', views.PedidoSingle, name='pedido'),
    path('sac.html/', views.sac, name="sac"),
    path('faq.html/', views.faq, name="faq"),
    path('favoritar/', views.Favoritar, name="favoritar"),
    path('ConsultarFavorito/', views.ConsultarFavorito, name="ConsultarFavorito"),
    path('MeusFavoritos.html/', views.MeusFavoritos, name="MeusFavoritos"),
    path("payment_form2.html", views.teste, name="teste"),
    path('rastrearentrega/<int:id>', views.Rastrearentrega, name="rastrearentrega"),
    path('pagarpedido/<int:id><int:method>', views.Pagarpedido, name="pagarpedido"),
    path('cadastrarAvaliacao/<int:id>', views.CadastrarAvaliacao, name='cadastrarAvaliacao'),
    path('productstag/<str:tag>', views.productstag, name='productstag'),
    path('productsmat/<str:mat>', views.productsmat, name='productsmat'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('desconto/', views.Desconto, name='desconto'),
    ]

    
    
