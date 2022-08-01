from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginCliente
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models.query_utils import Q, PathInfo
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.functional import empty
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timezone, timedelta
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core.paginator import Paginator

from payments.models import Payment
from users.models import *
from produtos.models import *
from pedidos.models import *
from outros.models import *

import requests
import xml.etree



#Funções para templates que não necessitam de login/autenticação

def handle_not_found(request, exception):
    return render(request, "pages/404.html")

def teste(request):
    publishable_key = settings.MERCADO_PAGO_PUBLIC_KEY #seta a chave publica para a pagina
    return render(request, "pages/payment_form2.html", {'publishable_key':publishable_key})

def faq(request):
    return render(request, "pages/faq.html")    

@require_POST
@csrf_exempt
def Desconto(request):
    try:
        id_cliente = request.user.id
        clienteDados = User.objects.filter(id = id_cliente)
        cod = request.POST.get('valor')       
        cup = Cupons.objects.get(cupom=cod)
        
        cpcl = Cupon_cliente.objects.filter(Q(cupom=cup) & Q(cliente=id_cliente))
        
        if not cpcl:
            msg = cup.desconto
            
        else:    
            raise ValueError

    except:
        msg = "Cupom inválido ou já foi utilizado!"    

    return JsonResponse({'msg':msg})
   

def carrinho(request):
    if request.user.is_authenticated:
        try:

            id_cliente = request.user.id #captura o id do usuário
            enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
            
            return render(request, 'pages/carrinho.html', {'enderecos':enderecosSalvos})

        except:
            return render(request, 'pages/index.html')    
    else:
        return render(request, 'pages/carrinho.html')

@csrf_exempt
@require_POST
def newsletter(request):
    emailnews = str(request.POST.get('valor'))
    emailfinal = emailnews[6:].replace("%40","@")
    
    cadastrar = Newsletter.objects.create(email=emailfinal)
    cadastrar.save

    return JsonResponse({})

@csrf_exempt
@require_POST
def calcular(request):
    url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?nCdEmpresa=&sDsSenha=&sCdAvisoRecebimento=n&sCdMaoPropria=n&nVlValorDeclarado=0&nVlDiametro=0&StrRetorno=xml&nIndicaCalculo=3&sCepOrigem=06730000&nVlComprimento=20&nVlAltura=10&nVlLargura=10&nCdFormato=1&nVlPeso=1&'

    variaveisExtras = request.POST.get('valor')
    urlFinal = url+variaveisExtras+'&nCdServico=04014'
    urlFinal2 = url+variaveisExtras+'&nCdServico=04510'
    
    try:    
        res = requests.get(urlFinal)
        fin =  xml.etree.ElementTree.XML(res.content)
        res2 = requests.get(urlFinal2)
        fin2 =  xml.etree.ElementTree.XML(res2.content)

        valor = (fin[0][1].text)
        prazo = (fin[0][2].text)
        valor2 = (fin2[0][1].text)
        prazo2 = (fin2[0][2].text)
        
    except:

        valor = 'CEP NÃO ENCONTRADO'
        prazo = ''
        valor2 = 'CEP NÃO ENCONTRADO'
        prazo2 = ''
    

    return JsonResponse({'valor':valor, 'prazo':prazo, 'valor2':valor2, 'prazo2':prazo2})

@csrf_exempt
@require_POST
def consultarEstoque(request):
        
    id = request.POST.get('id')
    try:
        estoque = Estoque.objects.values_list('qtd').get(id_variacaoProduto = id)
    except:
        estoque = 0  
        
    return JsonResponse({'estoque':estoque})

def vazio(request): #Função para redirecionar para a tela inicial do site 
    return render(request, 'pages/index.html', {'login':"login"}) # se não estiver logado na sessao vai para o index com o login no header
  
def index(request): #Função para redirecionar para a tela inicial do site

    return render(request, 'pages/index.html') # se não estiver logado na sessao vai para o index com o login no header

def contact(request): #Função para redirecionar para a tela de contato da empresa/site
    return render(request, 'pages/contact.html')

def products(request, categoria):  #Função para redirecionar para a tela de produtos

    try:
        variacoes = [] #cria lista vazia para armazenar os produtos de determinadas categoria
        listaDeSub = []
        listadeProd = []
        
        
        if categoria == 'allaneis': #se for todos produtos de aneis
            
            cat = Categoria.objects.get(nome='Aneis') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir 

        elif categoria == 'allaliancas': #se for todos produtos de aneis

            cat = Categoria.objects.get(nome='Aliancas') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == 'allcolares': #se for todos produtos de aneis

            cat = Categoria.objects.get(nome='Colares') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    


            cat = Categoria.objects.get(nome='Aliancas') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == 'allpingentes': #se for todos produtos de aneis

            cat = Categoria.objects.get(nome='Pingentes') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == 'allpulseiras': #se for todos produtos de aneis

            cat = Categoria.objects.get(nome='Pulseiras') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == 'allbrincos': #se for todos produtos de aneis

            cat = Categoria.objects.get(nome='Brincos') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == 'allberloques': #se for todos produtos de aneis

            cat = Categoria.objects.get(nome='Berloques') #pega a categoria certa
            
            for sub in Subcategoria.objects.filter(id_categoria=cat.id_categoria):
                listaDeSub.append(sub) #adiciona na lista de subcategorias da categoria
                
            for x in listaDeSub:
                id = x.id_subcategoria
                prods = Produto.objects.filter(id_subcategoria=id) #para cada subcategoria busca os produtos
                if prods:
                    listadeProd.append(Produto.objects.filter(id_subcategoria=id)) #adiciona na lista de produtos o produto
                
                                        

            for prod in listadeProd:
                for p in prod:
                    id = p.id_produto
                    for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                        variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == 'all': #Todos produtos do site
            
            for var in (VariacaoProduto.objects.all().select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir    

        elif categoria == "" or categoria == None: #se for vazio a categoria
            variacoes = []

        else:  #se passar subcategoria especifica   
            
            sub = Subcategoria.objects.get(nome=categoria) #pega o id da categoria que irá filtrar
            id = sub.id_subcategoria

            for prod in Produto.objects.filter(id_subcategoria=id): #filtra produtos e faz loop  
                id = prod.id_produto
                for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                    variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir   
        
        paginator = Paginator(variacoes,30)
        page = request.GET.get('page')
        variac = paginator.get_page(page)

        return render(request, 'pages/products.html', {'produtos':variac, 'variacoes':variacoes})
    except:
        return render(request, 'pages/products.html', {'msg': 'Erro ao pesquisar os produtos'})    

def productstag(request, tag):  #Função para redirecionar para a tela de produtos

    try:
        variacoes = [] #cria lista vazia para armazenar os produtos de determinadas categoria
        

        tagg = Tag.objects.get(tag=tag)
        prods = Produto_Tag.objects.filter(id_tag=tagg) #pega o id da categoria que irá filtrar
        
        for prod in prods: #filtra produtos e faz loop  
            id = prod.id_produto
            for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir   
        
        paginator = Paginator(variacoes,30)
        page = request.GET.get('page')
        variac = paginator.get_page(page)
        return render(request, 'pages/products.html', {'produtos':variac, 'variacoes':variacoes})

    except:
        return render(request, 'pages/products.html', {'msg': 'Erro ao pesquisar os produtos'})

def productsmat(request, mat):  #Função para redirecionar para a tela de produtos

    try:
        variacoes = [] #cria lista vazia para armazenar os produtos de determinadas categoria
        

        matt = Material.objects.get(descricao=mat)
        prods = Produto_Material.objects.filter(id_material=matt) #pega o id da categoria que irá filtrar
        
        for prod in prods: #filtra produtos e faz loop  
            id = prod.id_produto
            for var in (VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto')):
                variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir   
        
        paginator = Paginator(variacoes,30)
        page = request.GET.get('page')
        variac = paginator.get_page(page)

        return render(request, 'pages/products.html', {'produtos':variac, 'variacoes':variacoes})
    except:
        return render(request, 'pages/products.html', {'msg': 'Erro ao pesquisar os produtos'})

def buscarProduto(request): #Função para pesquisar produtos que usuario colocou na barra de search

    search = request.GET.get('search') #pega o texto do usuario
    variacoes = [] #cria lista de produtos
    msg = ''

    try:
        verificacao = Produto.objects.filter(nome__icontains=search)
        if verificacao:
            for prod in Produto.objects.filter(nome__icontains=search): #pesquisa
                id = prod.id_produto #pega o id do produto
                for var in VariacaoProduto.objects.filter(id_produto=id).select_related('id_produto').order_by('id_produto','preco').distinct('id_produto'): #pega as variacões
                    variacoes.append(var) #adiciona na lista as variacoes, a com menor preco apenas para exibir 
                    
        else:            
            msg = 'Nenhum produto encontrado'   
            
                   
    except:
       msg = 'Nenhum produto encontrado'
       
            
    return render(request, 'pages/products.html', {'produtos':variacoes})#redireciona a tela de produtos 

def account(request): #Função para redirecionar para a tela de cadastro de conta de usuario/cliente

    if request.user.is_authenticated: #verifica se usuário está autenticado
        
        try:

            id_cliente = request.user.id #captura o id do usuário
           
            enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
            telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
            clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
            
                                  
            return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados, 'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

        except: #se algum erro ocorrer...

            return render(request, 'pages/meusdados.html') # redireciona para a tela da 'minha conta' caso usuario já esteja logado
        
    return render(request, 'pages/account.html') #redireciona para account e passa o parametro login no header

def login(request): #Função para redirecionar para a tela de login do usuário/cliente
        
    if request.user.is_authenticated: #verifica se usuário está autenticado/logado
        return render(request, 'pages/index.html') #redireciona para a tela inicial se usuário estiver logado com os parametros no header

    else:
        return render(request, 'pages/login.html') #se não estiver logado redireciona para a tela de login

def resetPassword1(request):
    return render(request, 'pages/resetPassword1.html')

def resetPassword2(request):
    return render(request,'pages/resetPassword2.html')

def single(request, id): #Função para redirecionar para a tela do produto 
     
    try:
        produtoExibir = Produto.objects.get(id_produto=id)
        variacoes = VariacaoProduto.objects.select_related('id_cor', 'id_tamanho', 'id_produto').filter(id_produto=id)
        materiais = Produto_Material.objects.filter(id_produto=id)
        tags = Produto_Tag.objects.filter(id_produto=id)
        fotos = fotosProduto.objects.filter(id_produto=id)
        reviews = Review.objects.select_related('usuario').filter(id_produto=id)
        fivestar = 0
        fourstar = 0
        threestar = 0
        twostar = 0
        onestar = 0
        valortotal = 0
        qtdreviews = len(reviews)
        
        for r in reviews:
            valor = r.rating
            valortotal += valor
            if valor == 1:
                onestar += 1
            elif valor == 2:
                twostar += 1
            elif valor == 3:
                threestar += 1   
            elif valor == 4:
                fourstar += 1
            elif valor == 5:
                fivestar += 1

        if qtdreviews ==0:
            qtdreviews = 1
        mediareviews = (valortotal)/qtdreviews  
        mediarating = (mediareviews)
        porcento1 = (onestar*100)/qtdreviews
        porcento2 = (twostar*100)/qtdreviews
        porcento3 = (threestar*100)/qtdreviews
        porcento4 = (fourstar*100)/qtdreviews
        porcento5 = (fivestar*100)/qtdreviews
                

        return render(request, 'pages/single.html', {'prod':produtoExibir, 'variacoes':variacoes, 'materiais':materiais, 'tags':tags, 'fotos':fotos, 'reviews':reviews, 'onestar':onestar, "twostar":twostar, "threestar":threestar, "fourstar":fourstar, "fivestar":fivestar, 'qtdreviews':(len(reviews)),'mediarating':mediarating, 'porcento1':porcento1,'porcento2':porcento2,'porcento3':porcento3,'porcento4':porcento4,'porcento5':porcento5}) 

    except:   
    
    
        return render(request, 'pages/products.html', {'mgs':'Algum erro ocorreu'}) 
                  
@require_POST 
def cadastarCliente(request): #Função para cadastrar um novo usuário (cliente)

    
    try:
        cliente_aux = User.objects.get(email=request.POST['email']) #verifica se já existe esse email cadastrado
        if cliente_aux: #verifica se o cliente_aux está vazio ou não (se estiver é porque nao encontrou o email cadastrado)
            return render(request, 'pages/account.html', {'msg': 'Erro! Já existe um usuário cadastrado com o mesmo e-mail'}) #se encontrou email, envia mensagem para a tela avisando

    except User.DoesNotExist: #se o email nao existir...
        try:
            cliente_aux2 = User.objects.get(cpf=request.POST['cpf']) #verifica se o cpf já esta cadastrado
            if cliente_aux2:
             return render(request, 'pages/account.html', {'msg': 'Erro! Já existe um usuário cadastrado com o mesmo CPF'}) # se já estiver cadastrado enviará mensagem avisando
        
        except: # se tudo estiver ok irá pegar os parametros enviados no formulario

            
                nome_cliente = request.POST["nome"]
                sobrenome_cliente = request.POST["sobrenome"]
                sexo_cliente = request.POST["sexo"]
                datanascimento_cliente = request.POST["nascimento"]
                cpf_cliente = request.POST["cpf"]
                email_cliente = request.POST["email"]
                email2_cliente = request.POST["email2"]
                senha_cliente = request.POST["senha"]
                senha2_cliente = request.POST["senha2"]
                cep_cliente = request.POST["cep"]
                cidade_cliente = request.POST['cidade']
                rua_cliente = request.POST['rua']
                numero_cliente = request.POST['numero']
                bairro_cliente = request.POST['bairro']
                estado_cliente = request.POST['uf']
                complemento1_cliente = request.POST['complemento1']
                complemento2_cliente = request.POST['complemento2']
                telefone_cliente = request.POST["telefone"]
                news = request.POST.get('newslettercheck', 'False')
                
                if news == 'True':
                    try:
                        cadastrar = Newsletter.objects.create(email=email_cliente)
                        cadastrar.save
                    except:
                        a = 'ja cadastrado'    
                    
            

                if (nome_cliente or sobrenome_cliente or sexo_cliente or datanascimento_cliente or cpf_cliente or email_cliente or email2_cliente or senha_cliente or senha2_cliente or cep_cliente or cidade_cliente or rua_cliente or numero_cliente or bairro_cliente or estado_cliente or telefone_cliente ) == None or (nome_cliente or sobrenome_cliente or sexo_cliente or datanascimento_cliente or cpf_cliente or email_cliente or email2_cliente or senha_cliente or senha2_cliente or cep_cliente or cidade_cliente or rua_cliente or numero_cliente or bairro_cliente or estado_cliente or telefone_cliente ) == "":
                    return render(request, 'pages/account.html', {'msg': 'Erro! Por favor preencha todos dados obrigatórios'}) # se já estiver cadastrado enviará mensagem avisando
                else:    
                    senhaHash = make_password(senha_cliente) #cria uma senha hash para salvar no banco de dados

                    novoCliente = User.objects.create(
                    username=email_cliente,
                    first_name=nome_cliente,
                    last_name=sobrenome_cliente,
                    sexo=sexo_cliente,
                    datanascimento=datanascimento_cliente, 
                    cpf=cpf_cliente,
                    email=email_cliente,
                    password=senhaHash
                    )
                    novoCliente.save() # salva o cadastro no banco de dados


                    clienteFim = User.objects.get(username = email_cliente)
                    id_cliente = clienteFim.id
                    

                    novoEndereco = Endereco_cliente.objects.create( 

                        id_user_id = id_cliente,
                        cep = cep_cliente,
                        cidade = cidade_cliente,
                        rua = rua_cliente,
                        numero = numero_cliente,
                        bairro = bairro_cliente,
                        estado = estado_cliente,
                        complemento1 = complemento1_cliente,
                        complemento2 = complemento2_cliente
                        

                    )  #cria o novo endereco no banco de dados

                    novoEndereco.save() #salva 

                    novoTelefone = Telefone_cliente.objects.create(

                        id_user_id = id_cliente,
                        telefone = telefone_cliente
                        
                    
                        
                    ) #Cria novo telefone no banco de dados

                    novoTelefone.save() #salva

                    

                    return render(request, 'pages/login.html', {'msg':'Cadastro efetuado com sucesso! Efetue o login'}) # envia o usuário para tela de login e pede para ele logar
            
                return render(request, 'pages/login.html', {'msg':'Algum erro ocorreu durante o cadastro, tente novamente'})   
            
@require_POST
def logarCliente(request): #Função para efetuar o Login na sessao
        nxt = str(request.POST["next"])
        #captura os dados passados no formulario via post
        emailparalogar = request.POST['email'] 
        senhaparalogar = request.POST['senha']
       
        if (emailparalogar or senhaparalogar) == None or (emailparalogar or senhaparalogar) == "":
            return render(request, 'pages/login.html', {'msg':'Por favor preencha os campos!'}) #envia mensagem para tela de login avisando que login ou senha estão incorretos
        cliente = authenticate(username=emailparalogar, password=senhaparalogar) #verifica a senha e o username se estão corretos

        if cliente is not None: # se ele verificar que está correto executa 

            loginCliente(request, cliente) #efetua o login do cliente
            if request.user.is_authenticated: #verifica se está logado

                nome =request.user.first_name #captura o nome do cliente
                if len(nxt)==0:
                    return render(request, 'pages/index.html', {'cliente':nome, 'logout':'| logout'}) #redireciona para tela next e  logado na sessao
                elif nxt is not None:
                    
                    if nxt == '/meusdados.html/':
                        try:
                            
                            id_cliente = request.user.id #captura o id do usuário
                        
                            enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                            telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
                            clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
                             
                            return render(request, f'pages{nxt}', {'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para tela next e  logado na sessao
                        except:
                            return render(request, f'pages{nxt}') #redireciona para tela next e  logado na sessao  
                    else:     
                        return render(request, f'pages{nxt}') #redireciona para tela next e  logado na sessao  
                return render(request, 'pages/index.html') #redireciona para tela next e  logado na sessao
            else:
                return render(request, 'pages/login.html', {'msg':'Email e/ou senha incorretos'}) #envia mensagem para tela de login avisando que login ou senha estão incorretos

        return render(request, 'pages/login.html', {'msg':'Email e/ou senha incorretos'}) #envia mensagem para tela de login avisando que login ou senha estão incorretos





#Funções para templates que necessitam de login/autenticação

@login_required
def sac(request):
    return render(request, "pages/sac.html")

@csrf_exempt
@require_POST
def checkout(request):#Função para redirecionar para a tela de checkout / carrinho de compras

    if request.user.is_authenticated:

        try: 
            carrinho = request.POST
            qtd = carrinho.get('itemCount')
            if qtd == 0:
                return render(request, 'pages/carrinho.html', {'msg':'O carrinho está vazio!'})

            idendereco = carrinho.get('endereco')
            idfrete = int(carrinho.get('frete'))

            if idfrete > 3 or idfrete < 1:

                id_cliente = request.user.id #captura o id do usuário
                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                return render(request, 'pages/carrinho.html', {'enderecos':enderecosSalvos, 'msg':'Algum erro ocorreu!'})

            else:
                items = []
                totalprodutos = 0
                totalpedido = 0
                
                endereco = Endereco_cliente.objects.get(id_endereco = idendereco)
                endcep = endereco.cep
                
                cep = 'sCepDestino='+endcep
                
                for i in range(int(qtd)):
                    idvar = carrinho.get(f'item_idvar_{i+1}')
                    qtdvar = carrinho.get(f'item_quantity_{i+1}')
                    var = VariacaoProduto.objects.select_related('id_produto').get(id_variacao = idvar)
                    subtotal = (var.preco)*int(qtdvar)
                    totalprodutos += subtotal
                    itempedido = {'qtdvar':qtdvar, 'var':var, 'subtotal':subtotal}
                    items.append(itempedido)
                    

                    
                url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?nCdEmpresa=&sDsSenha=&sCdAvisoRecebimento=n&sCdMaoPropria=n&nVlValorDeclarado=0&nVlDiametro=0&StrRetorno=xml&nIndicaCalculo=3&sCepOrigem=06730000&nVlComprimento=20&nVlAltura=10&nVlLargura=10&nCdFormato=1&nVlPeso=1&'

                if idfrete == 1:
                    urlFinal = url+cep+'&nCdServico=04014'
                    opcao = 'Sedex'

                elif (idfrete == 2):
                    urlFinal = url+cep+'&nCdServico=04510'
                    opcao = 'Pac'

                elif (idfrete == 3):    
                    urlFinal = url+cep+'&nCdServico=04510'
                    opcao = 'Grátis'
                                
                try:    
                    res = requests.get(urlFinal)
                    fin =  xml.etree.ElementTree.XML(res.content)
                    valor = (fin[0][1].text)
                    prazo = (fin[0][2].text)
                    
                    valor = valor.replace(',', '.')

                    if (idfrete == 3):
                        valor = 0
                        
                    totalpedido = float(valor) + float(totalprodutos)
                    totalpedido = '{:.2f}'.format(totalpedido)
                    
                except:

                    valor = 'CEP NÃO ENCONTRADO'
                    prazo = ''

                    
        except:
            try:
                id_cliente = request.user.id #captura o id do usuário
                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                return render(request, 'pages/carrinho.html', {'enderecos':enderecosSalvos, 'msg':'Algum erro ocorreu na finalização do pedido, tente novamente mais tarde, e se o problema persistir, entre em contato conosco'})
            except:    
                return render(request, 'pages/carrinho.html', {'msg':'Algum erro ocorreu na finalização do pedido, tente novamente mais tarde, e se o problema persistir, entre em contato conosco'})            
    else:
         return render(request, 'pages/login.html', {'msg':'Por favor efetue o login para efetuar a compra'})
    
    return render(request, 'pages/checkout.html', {'endereco':endereco, 'items':items, 'qtd':qtd, 'totalprodutos':totalprodutos, 'idfrete':idfrete, 'valor':valor, 'prazo':prazo, 'opcao':opcao, 'totalpedido':totalpedido})

@login_required   
@require_POST
def finalizarPedido(request):
    if request.user.is_authenticated:
        id_cliente = request.user.id

                        
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente)
        clienteDados = User.objects.filter(id = id_cliente)

    
        all = request.POST
        idcliente = request.POST.get('idcliente')
        enderecoentrega = request.POST.get('enderecoentrega')
        idfrete = request.POST.get('idfrete')
        idfrete = int(idfrete)
        items = all.getlist('items')
        tipopagamento = request.POST.get('pagamentoescolhido')
        
        try:
            if (all or idcliente or enderecoentrega or idfrete or items) is not None:
                
                url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?nCdEmpresa=&sDsSenha=&sCdAvisoRecebimento=n&sCdMaoPropria=n&nVlValorDeclarado=0&nVlDiametro=0&StrRetorno=xml&nIndicaCalculo=3&sCepOrigem=06730000&nVlComprimento=20&nVlAltura=10&nVlLargura=10&nCdFormato=1&nVlPeso=1&'

                endereco = Endereco_cliente.objects.get(id_endereco = enderecoentrega)
                endcep = endereco.cep
                cep = 'sCepDestino='+endcep
                
                    
                if idfrete == 1:
                    urlFinal = url+cep+'&nCdServico=04014'
                    
                elif (idfrete == 2):
                    urlFinal = url+cep+'&nCdServico=04510'
                    
                elif (idfrete == 3):
                    valor = 0
                
                if idfrete ==1 or idfrete ==2:    
                    
                    try:    
                        
                        res = requests.get(urlFinal)
                        fin =  xml.etree.ElementTree.XML(res.content)
                        valor = (fin[0][1].text)                  
                        valor = valor.replace(',', '.')   
                                                        
                                                
                    except:
                        
                        return render(request, 'pages/carrinho.html', {'msg':'Algum erro ocorreu durante o processamento, tente novamente mais tarde, e se os problemas persistirem, por favor entre em contato conosco!'})

                
                cliente = User.objects.get(id=id_cliente)
                endereco = Endereco_cliente.objects.get(id_endereco=enderecoentrega)
                statu = Status.objects.get(id_status = 1)     
                
                
                idnovoPedido = Pedido.objects.create(id_cliente=cliente,id_endereco=endereco,frete=valor,opcaofrete=idfrete, status_pedido=statu).pk
                
                novoPedido = Pedido.objects.get(numero_pedido=idnovoPedido)
                
                try:

                    codg = request.POST.get('codpromo')
                    cup = Cupons.objects.get(cupom=codg)
                    

                    cpcl = Cupon_cliente.objects.filter(Q(cupom=cup) & Q(cliente=id_cliente))
            
                    if not cpcl:
                        desc = cup.desconto
                    else:    
                        raise ValueError
                
                except:

                    desc = 0            
                

                for item in items:
                    item = item.split(',')
                    variacao = VariacaoProduto.objects.get(id_variacao=item[0])
                    val = variacao.preco
                    

                    if desc > 0:
                        val = (variacao.preco)-(variacao.preco)*(desc/100)

                    ItemPedido.objects.create(
                        id_pedido=novoPedido,
                        id_produto=variacao,
                        preco= val,
                        qtd=item[1],
                    )

                request.session['order_id'] = idnovoPedido
                request.session['pay_method'] = tipopagamento

                try:
                    salvar = Cupon_cliente.objects.create(cupom= cup, cliente = clienteDados)
                    salvar.save()
                except:
                    salvar = 0
                
                return redirect(reverse("payments:process"))

            else:
                return render(request, 'pages/carrinho.html', {'mgs':'Erro ao finalizar, carrinho está vazio', 'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados})
        except:
            return render(request, 'pages/carrinho.html', {'msg':'Algum erro ocorreu durante o processamento, tente novamente mais tarde, e se os problemas persistirem, por favor entre em contato conosco!', 'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados})
    else:
        return render(request, 'pages/login.html', {'msg':'Por favor, efetue o login'})

@login_required   
@require_POST
@csrf_exempt
def Favoritar(request):
    valor = str(request.POST.get('valor'))
    id = valor[4:]
    id_cliente = request.user.id
    client = User.objects.get(id=id_cliente)
    prod = Produto.objects.get(id_produto=id)

    if Favoritos.objects.filter(cliente=client, produto = prod):
        Favoritos.objects.filter(cliente=client, produto = prod).delete()
        resposta = 1

    else:    
        favorito = Favoritos.objects.create(cliente=client, produto = prod)
        favorito.save()
        resposta = 2
        
    return HttpResponse({resposta})

@login_required   
def meusPedidos(request):
    if request.user.is_authenticated: #verifica se usuário está autenticado/logado
        
        try:

            id_cliente = request.user.id #captura o id do usuário
          
            pedidosSalvos = Pedido.objects.select_related('id_endereco').filter(id_cliente=id_cliente)

                                    
            return render(request, 'pages/meusPedidos.html',{'pedidos':pedidosSalvos}) #redireciona para meusdados com todos as informações

        except: #se algum erro ocorrer...
            

            return render(request, 'pages/meusPedidos.html') #redireciona para a tela 'minhaconta'

    else:
        return render(request, 'pages/login.html', {'msg':'Por favor efetue o login!'}) #caso não esteja logado redireciona para tela de login e pede para logar

@login_required   
def PedidoSingle(request, id):
    if request.user.is_authenticated: 
        
        id_cliente = request.user.id
        pedido = Pedido.objects.select_related('id_endereco', 'status_pedido').get(numero_pedido=id)
        items = ItemPedido.objects.filter(id_pedido=id).select_related('id_produto').select_related('id_produto')
        pags = Payment.objects.filter(order=id)
        order = get_object_or_404(Pedido, numero_pedido = id)
        valortotal = order.get_preco_total()
        valorcomfrete= order.frete+valortotal
    
        
        return render(request, 'pages/Pedido.html', {'pedido':pedido, 'items':items, 'pags':pags, 'valortotal':valortotal, 'valorcomfrete':valorcomfrete}) #caso não esteja logado redireciona para tela de login e pede para logar

    else:    
        return render(request, 'login/.html', {'msg':'Por favor efetue o login!'}) #caso não esteja logado redireciona para tela de login e pede para logar

@login_required   
@require_POST
@csrf_exempt
def ConsultarFavorito(request):
    
    id = str(request.POST.get('valor'))
    id_cliente = request.user.id

    client = User.objects.get(id=id_cliente)
    prod = Produto.objects.get(id_produto=id)

    if Favoritos.objects.filter(cliente=client, produto = prod):
        resposta = 1

    else:    
        resposta = 2


    return HttpResponse(resposta)

@login_required
def alterarFrm(request): #Função para redirecionar para tela de alterar a senha de login do usuário
    if request.user.is_authenticated: #verifica se usuário está autenticado
        
        return render(request, 'pages/alterarFrm.html') #redireciona para a tela de alterar a senha

    return render(request, 'pages/index.html')  #redireciona para a tela de login e exige login

@login_required
def meusdados(request): #Função para redirecionar para tela meusdados e trazer informações do usuário na tela
    if request.user.is_authenticated: #verifica se usuário está autenticado/logado
        
        try:

            id_cliente = request.user.id #captura o id do usuário
           
            enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
            telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
            clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
            
                                  
            return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

        except: #se algum erro ocorrer...
            

            return render(request, 'pages/meusdados.html') #redireciona para a tela 'minhaconta'

    else:
        return render(request, 'pages/login.html', {'msg':'Por favor efetue o login!'}) #caso não esteja logado redireciona para tela de login e pede para logar

@login_required
def enderecos(request):  #Função para redirecionar para tela de cadastro de enderecos do cliente
    if request.user.is_authenticated: #verifica se usuário está autenticado
                                
        return render(request, 'pages/enderecos.html' ) #redireciona para enderecos e passa o parametro login no header

    return render(request, 'pages/login.html') #redireciona para login e passa o parametro login no header

@login_required
def telefones(request): #Função para redirecionar para tela de cadastro de telefone de cliente
    if request.user.is_authenticated: #verifica se usuário está autenticado
                
        return render(request, 'pages/telefones.html')#redireciona para telefones e passa o parametro login no header

    return render(request, 'pages/login.html') #redireciona para login e passa o parametro login no header
    
@login_required
def sair(request): #Função para efetuar o Logout da sessao
    if request.user.is_authenticated == True: #verifica se usuario está logado na sessao
        logout(request) #efetua o logout/sai da sessao
        return HttpResponseRedirect('/')  #redireciona para a tela inicial do site
    
    return render(request, 'pages/index.html')  #redireciona para a tela de login e exige login

@require_POST
@login_required
def alterar_senha(request): #Função para efetuar a troca de senha do usuário
    if request.user.is_authenticated: #verifica se está logado na sessão
        
        email = request.user.username #pega o username do usuario logado

        senhaDigitada = request.POST['senhaatual'] #pega via post a senha antiga/atual
        
        novaSenha = request.POST['novasenha'] #pega via post a nova senha
        
        if (senhaDigitada or novaSenha) is not None or (senhaDigitada or novaSenha) != '':

            try:
                if request.user.check_password(senhaDigitada): #verifica se a senha antiga/atual está correta

                    clienteFim = User.objects.get(username=email) #pega o usuario com o username passado
                    clienteFim.set_password(novaSenha) #atribui a nova senha
                    clienteFim.save() #salva
                    
                    #usuario é desconectado

                    return render(request, 'pages/login.html', {'msg':'Efetue o login novamente'}) #redireciona oara login e exije que se autentique novamente
            except:
                
                return render(request, 'pages/alterarFrm.html', {'msg':'Algum erro ocorreu, sua senha não foi alterada, efetue o login e certifique-se que preencheu corretamente a senha antiga'}) #redireciona oara login e exije que se autentique novamente
        else:
            return render(request, 'pages/alterarFrm.html', {'msg':'Algum erro ocorreu, sua senha não foi alterada, efetue o login e certifique-se que preencheu corretamente as senhas'}) #redireciona oara login e exije que se autentique novamente

    
    return render(request, 'pages/alterarFrm.html', {'msg':'Algum erro ocorreu, sua senha não foi alterada, efetue o login e certifique-se que preencheu corretamente a senha antiga'})

@login_required
def cadastrarEndereco(request): #Função para cadastrar endereço novo para o usuário/cliente do site
    if request.user.is_authenticated: #verifica se está autenticado
        
        #pega os dados enviados via POST
        try:
            id_cliente = request.user.id
            cep_cliente = request.POST["cep"]
            cidade_cliente = request.POST['cidade']
            rua_cliente = request.POST['rua']
            numero_cliente = request.POST['numero']
            bairro_cliente = request.POST['bairro']
            estado_cliente = request.POST['uf']
            complemento1_cliente = request.POST['complemento1']
            complemento2_cliente = request.POST['complemento2']

            if (id_cliente, cep_cliente,cidade_cliente, rua_cliente,numero_cliente, bairro_cliente,estado_cliente) == None or (id_cliente, cep_cliente,cidade_cliente, rua_cliente,numero_cliente, bairro_cliente,estado_cliente) == "":
                    return render(request, 'pages/enderecos.html', {'msg': 'Erro! Por favor preencha todos dados obrigatórios'}) # se já estiver cadastrado enviará mensagem avisando
            else:  
           
                novoEndereco = Endereco_cliente.objects.create( 

                    id_user_id = id_cliente,
                    cep = cep_cliente,
                    cidade = cidade_cliente,
                    rua = rua_cliente,
                    numero = numero_cliente,
                    bairro = bairro_cliente,
                    estado = estado_cliente,
                    complemento1 = complemento1_cliente,
                    complemento2 = complemento2_cliente
                    

                )  #cria o novo endereco no banco de dados

                novoEndereco.save() #salva       

                id_cliente = request.user.id
                        
                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
                telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente)
                clienteDados = User.objects.filter(id = id_cliente)

                #pega os dados do usuario logado para redirecionar para tela de meusdados novamente e mostrar as informações
                                    
                return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados})

                

        except: #se algum erro ocorrer...
                
                return render(request, 'pages/meusdados.html')

    else:
        return render(request, 'pages/login.html', {'msg':'Efetue o login por favor!'})  #caso não esteja autenticado redireciona para a tela de login

@login_required
def cadastrarTelefone(request): #Função para cadastrar novo telefone para o usuário/cliente logado no site

    if request.user.is_authenticated: #verifica se está autenticado
                
        try:
            id_cliente = request.user.id

            #pega os dados enviados via POST

            telefone_cliente = request.POST["telefone"]
            
            if (telefone_cliente) == None or (telefone_cliente) == "":
                    return render(request, 'pages/telefones.html', {'msg': 'Erro! Por favor preencha todos dados obrigatórios'}) # se já estiver cadastrado enviará mensagem avisando
            else:  
           
                novoTelefone = Telefone_cliente.objects.create(

                    id_user_id = id_cliente,
                    telefone = telefone_cliente
                    
                
                ) #Cria novo telefone no banco de dados

                novoTelefone.save() #salva

                
                
                try:#pega os dados do usuario logado para redirecionar para tela de meusdados novamente e mostrar as informações
                    enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
                    telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente)
                    clienteDados = User.objects.filter(id = id_cliente)
                                            
                    return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados})

                except: #se algum erro ocorrer...
                

                    return render(request, 'pages/meusdados.html')

        except:
            

            return render(request, 'pages/meusdados.html') #se usuário não estiver autenticado exije o login na tela de login

    else:
        return render(request, 'pages/login.html', {'msg':'Efetue o login por favor!'}) 

@login_required
def excluirTelefone(request, id): #Função para excluir um telefone do usuário cadastrado no site
    if request.user.is_authenticated: #verifica se usuário está autenticado
        
        id_cliente = request.user.id #pega o id do usuário

        #pega os dados do usuário, telefones e endereços
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente)
        clienteDados = User.objects.filter(id = id_cliente)
        
        if len(telefonesSalvos) <=1:#verifica se só existe 1 ou menos telefones cadastrados, se sim, não permite a exclusão para manter pelo menos 1 registro no banco de dados
            return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados, 'msg1':' É obrigatório ter pelo menos um telefone cadastrado'}) #redireciona novamente para a tela com os dados atualizados
        else:
            try: 

                deletar = Telefone_cliente.objects.get(id_telefone=id) #procura o registro desse telefone
                deletar.delete() #deleta o telefone
                
                telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #Consulta os telefones salvos
                clienteDados = User.objects.filter(id = id_cliente) #verifica os dados do cliente

                return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados}) #redireciona novamente para a tela com os dados atualizados
            

            except:    #se algum erro ocorrer...
            
                return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados}) #volta para o que estava
            

    else:
     return render(request, 'pages/login.html', {'msg':'Efetue o login por favor!'}) #se usuário não estiver autenticado exije que se autentique

@login_required
def excluirEndereco(request, id): #Função para excluir um endereco do usuário cadastrado no site
    if request.user.is_authenticated: #verifica se usuário está autenticado
        
        id_cliente = request.user.id #pega o id do usuário

        #pega os dados do usuário, telefones e endereços
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente)
        clienteDados = User.objects.filter(id = id_cliente)
        
        if len(enderecosSalvos) <=1: #verifica se só existe 1 ou menos enderecos cadastrados, se sim, não permite a exclusão para manter pelo menos 1 registro no banco de dados
            return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados, 'msg2':' É obrigatório ter pelo menos um endereço cadastrado'}) #redireciona novamente para a tela com os dados atualizados
        else:
            try: 

                deletar = Endereco_cliente.objects.get(id_endereco=id) #procura o registro desse endereco
                
                deletar.delete() #deleta o endereco
                  
                #faz a consulta dos dados novamente aos deletar

                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
                clienteDados = User.objects.filter(id = id_cliente)

                return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados}) #redireciona novamente para a tela com os dados atualizados
                

            except:    #se algum erro ocorrer...
                
                return render(request, 'pages/meusdados.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados}) #volta para o que estava
            

    else:
     return render(request, 'pages/login.html', {'msg':'Efetue o login por favor!'}) #se usuário não estiver autenticado exije que se autentique

@login_required
def excluirEndereco2(request, id): #Função para excluir um endereco do usuário cadastrado no site
    if request.user.is_authenticated: #verifica se usuário está autenticado
        
        id_cliente = request.user.id #pega o id do usuário

        #pega os dados do usuário, telefones e endereços
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente)
        clienteDados = User.objects.filter(id = id_cliente)
        
        if len(enderecosSalvos) <=1: #verifica se só existe 1 ou menos enderecos cadastrados, se sim, não permite a exclusão para manter pelo menos 1 registro no banco de dados
            return render(request, 'pages/carrinho.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados, 'msg2':' É obrigatório ter pelo menos um endereço cadastrado'}) #redireciona novamente para a tela com os dados atualizados
        else:
            try: 

                deletar = Endereco_cliente.objects.get(id_endereco=id) #procura o registro desse endereco
                
                deletar.delete() #deleta o endereco
                  
                #faz a consulta dos dados novamente aos deletar

                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente)
                clienteDados = User.objects.filter(id = id_cliente)

                return render(request, 'pages/carrinho.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados}) #redireciona novamente para a tela com os dados atualizados
                

            except:    #se algum erro ocorrer...
                
                return render(request, 'pages/carrinho.html', {'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'dadosCliente':clienteDados}) #volta para o que estava
            

    else:
     return render(request, 'pages/login.html', {'msg':'Efetue o login por favor!'}) #se usuário não estiver autenticado exije que se autentique

@login_required
def editarEndereco(request, id):#Função para redirecionar para tela de editar um endereco do usuário cadastrado no site
        if request.user.is_authenticated: #verifica se usuário está autenticado
                        
            #pega os dados do endereco

            id_cliente = request.user.id #captura o id do usuário

            if id is not None:
           
                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
                clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
                
                
                try:
                    enderecoParaEditar = Endereco_cliente.objects.get(id_endereco = id)
                    

                    return render(request, 'pages/editarEndereco.html', { 'cep':enderecoParaEditar.cep, 'rua':enderecoParaEditar.rua,'numero':enderecoParaEditar.numero, 'bairro':enderecoParaEditar.bairro,'cidade':enderecoParaEditar.cidade, 'estado':enderecoParaEditar.estado,'complemento1':enderecoParaEditar.complemento1, 'complemento2':enderecoParaEditar.complemento2, 'idEndereco':enderecoParaEditar.id_endereco}) #redireciona para enderecos e passa o parametro login no header

                except: #se der erro...

                    return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'msg2':'Algum erro ocorreu, tente novamente agora ou mais tarde'}) #redireciona para meusdados com todos as informações

            else:
                return render(request, 'pages/index.html')

        else:
            return render(request, 'pages/login.html') 

@require_POST
@login_required
def salvarEnderecoEditado(request, id):

    if request.user.is_authenticated: #verifica se usuário está autenticado

        
        id_cliente = request.user.id #captura o id do usuário
        
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
        clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados

        #pega os dados enviados via POST
        
        try:

            cep_cliente = request.POST["cep"]
            cidade_cliente = request.POST['cidade']
            rua_cliente = request.POST['rua']
            numero_cliente = request.POST['numero']
            bairro_cliente = request.POST['bairro']
            estado_cliente = request.POST['uf']
            complemento1_cliente = request.POST['complemento1']
            complemento2_cliente = request.POST['complemento2']


            diferenca = timedelta(hours=-3) #calcula a diferenca de horario do padrao
            fusoHorario = timezone(diferenca) #aplica no fusohorario
            dataHoraAtual = datetime.now() #data e hora atual
            atualizadoEm = dataHoraAtual.astimezone(fusoHorario) #pega a hora correta de SP

            if (id_cliente, cep_cliente,cidade_cliente, rua_cliente,numero_cliente, bairro_cliente,estado_cliente) == None or (id_cliente, cep_cliente,cidade_cliente, rua_cliente,numero_cliente, bairro_cliente,estado_cliente) == "":
                    return render(request, 'pages/editarEndereco.html', {'msg': 'Erro! Por favor preencha todos dados obrigatórios'}) # se já estiver cadastrado enviará mensagem avisando
            else:  
           
                Endereco_cliente.objects.filter(id_endereco=id).update(rua=rua_cliente, cep=cep_cliente, cidade=cidade_cliente, numero=numero_cliente, bairro=bairro_cliente, estado=estado_cliente, complemento1=complemento1_cliente, complemento2=complemento2_cliente, atualizado=atualizadoEm) #faz um update no objeto selecionado

                #faz a consulta dos dados novamente aos deletar

                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
                clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
                                    
                return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

        except:

            return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

    else:

        return render(request, 'pages/login.html',{'msg':'Por favor, efetue o login'})
                
@login_required
def editarDados(request):#Função para redirecionar para tela de editar um dado do usuário cadastrado no site
        if request.user.is_authenticated: #verifica se usuário está autenticado
                        
            #pega os dados do endereco

            id_cliente = request.user.id #captura o id do usuário
           
            enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
            telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
            clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
            
            
            try:
                ClienteParaEditar = User.objects.get(id = id_cliente)
                

                return render(request, 'pages/editarDados.html', {'clienteed':ClienteParaEditar}) #redireciona para enderecos e passa o parametro login no header

            except: #se der erro...

                return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'msg2':'Algum erro ocorreu, tente novamente agora ou mais tarde'}) #redireciona para meusdados com todos as informações
        else:
            return render(request, 'pages/login.html', {'msg':'Por favor, efetue o login primeiro'})        

@require_POST
@login_required
def salvarDadosEditados(request): #Função para salvar dados do usuário que foram editados 

    if request.user.is_authenticated: #verifica se usuário está autenticado

        nome =request.user.first_name #pega o nome do usuário
        
        id_cliente = request.user.id #captura o id do usuário
        
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
        clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados

        #pega os dados enviados via POST
        
        try:

            nome_cliente = request.POST["nome"]
            sobrenome_cliente = request.POST['sobrenome']
            sexo_cliente = request.POST['sexo']
            data_cliente = request.POST['nascimento']
            
            if (nome_cliente,sobrenome_cliente,sexo_cliente,data_cliente,) == None or (nome_cliente,sobrenome_cliente,sexo_cliente,data_cliente,) == "":
                
                    return render(request, 'pages/editarDados.html', {'msg': 'Erro! Por favor preencha todos dados obrigatórios'}) # se já estiver cadastrado enviará mensagem avisando
            else:

                User.objects.filter(id=id_cliente).update(first_name = nome_cliente, last_name = sobrenome_cliente, sexo=sexo_cliente, datanascimento=data_cliente, ) #faz um update no objeto selecionado
                
                #faz a consulta dos dados novamente aos deletar

                enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
                clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
                                    
                return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

        except:

            return render(request, 'pages/meusdados.html',{ 'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

    else:

        return render(request, 'pages/login.html',{'msg':'Por favor, efetue o login'})
                
@login_required
def editarTelefone(request, id):#Função para redirecionar para tela de editar um telefone do usuário cadastrado no site

        if request.user.is_authenticated: #verifica se usuário está autenticado
                        
            #pega os dados do cliente

            id_cliente = request.user.id #captura o id do usuário
           
            enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
            telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
            clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
            
            if id is not None:

                try:

                    telefoneParaEditar = Telefone_cliente.objects.get(id_telefone = id)
                    
                    return render(request, 'pages/editarTelefone.html', {'telefone':telefoneParaEditar.telefone, 'idTelefone':telefoneParaEditar.id_telefone}) #redireciona para telefones e passa o parametro login no header

                except: #se der erro...

                    return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos, 'msg2':'Algum erro ocorreu, tente novamente agora ou mais tarde'}) #redireciona para meusdados com todos as informações

            else:
                return render(request, 'pages/index.html')

        else:
            return render(request, 'pages/login.html')        

@require_POST
@login_required
def salvarTelefoneEditado(request, id):

    if request.user.is_authenticated: #verifica se usuário está autenticado

        
        id_cliente = request.user.id #captura o id do usuário
        
        enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
        telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
        clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados

        #pega os dados enviados via POST
        
        if id is not None:
            try:

                telefone_editado = request.POST["telefone"]
                
                diferenca = timedelta(hours=-3) #calcula a diferenca de horario do padrao
                fusoHorario = timezone(diferenca) #aplica no fusohorario
                dataHoraAtual = datetime.now() #data e hora atual
                atualizadoEm = dataHoraAtual.astimezone(fusoHorario) #pega a hora correta de SP
                
                if telefone_editado is None or telefone_editado == "":
                    return render(request, 'pages/editarTelefone.html',{'msg':'O telefone não pode estar em branco'}) #redireciona para meusdados com todos as informações
                else:

                    Telefone_cliente.objects.filter(id_telefone=id).update(telefone=telefone_editado, atualizado=atualizadoEm) #faz um update no objeto selecionado

                    #faz a consulta dos dados novamente aos deletar

                    enderecosSalvos = Endereco_cliente.objects.filter(id_user_id = id_cliente) #verifica os enderecos salvos desse usuário no banco de dados
                    telefonesSalvos = Telefone_cliente.objects.filter(id_user_id = id_cliente) #verifica os telefones salvos desse usuário no banco de dados
                    clienteDados = User.objects.filter(id = id_cliente) #verifica os dados desse usuário no banco de dados
                                        
                    return render(request, 'pages/meusdados.html',{'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações

            except:

                return render(request, 'pages/meusdados.html',{ 'dadosCliente':clienteDados,  'enderecos':enderecosSalvos, 'telefones':telefonesSalvos}) #redireciona para meusdados com todos as informações
        else:

            return render(request, 'pages/index.html')


    else:

        return render(request, 'pages/login.html',{'msg':'Por favor, efetue o login'})
    
@login_required
def MeusFavoritos(request):

    if request.user.is_authenticated:
        try:
            id_cliente = request.user.id
            client = User.objects.get(id=id_cliente)
            favoritos = Favoritos.objects.filter(cliente = client).select_related('produto')
            
            return render(request, "pages/meusFavoritos.html", {'favoritos':favoritos})
        except:
            return render(request, "pages/index.html")
    else:

        return render(request, "pages/login.html, {'msg':'Por favor, efetue o login primeiro!'")

@login_required
def Rastrearentrega(request, id):
    
    return render(request, "pages/rastrearentrega.html")

@login_required   
def Pagarpedido(request, id, method):

    pay_method =  method
    order_id = id 
    order = get_object_or_404(Pedido, numero_pedido=order_id) 
    transaction_amount = order.get_preco_total()+order.frete #pega o valor total do pedido
    publishable_key = settings.MERCADO_PAGO_PUBLIC_KEY #seta a chave publica para a pagina
    request.session['order_id'] = order_id
    request.session['pay_method'] = pay_method
    
    
    if pay_method == 1:
         return render(request, 'pages/payment_form.html', {'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key}) #redireciona com os dados

    elif pay_method == 2:        
         return render(request, 'pages/payment_form2.html', {'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key}) #redireciona com os dados
    
    else:

        return render(request, 'pages/payment_form.html', {'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key}) #redireciona com os dados


@require_POST   
def CadastrarAvaliacao(request, id):
    if request.user.is_authenticated:
    
        ratingr = request.POST.get('rating')
        titulor = request.POST.get('titulo')
        descr = request.POST.get('descricao')

        prod = Produto.objects.get(id_produto=id)

        if ratingr and titulor and descr is not None:
            criarreview = Review.objects.create(usuario = request.user, rating=ratingr, descricao = descr, titulo = titulor, id_produto = prod)
            criarreview.save()
        else:
            return render(request, 'pages/products.html', {'mgs':'Algum erro ocorreu'})

        

        produtoExibir = Produto.objects.get(id_produto=id)
        variacoes = VariacaoProduto.objects.select_related('id_cor', 'id_tamanho', 'id_produto').filter(id_produto=id)
        materiais = Produto_Material.objects.filter(id_produto=id)
        tags = Produto_Tag.objects.filter(id_produto=id)
        fotos = fotosProduto.objects.filter(id_produto=id)
        reviews = Review.objects.select_related('usuario').filter(id_produto=id)
        fivestar = 0
        fourstar = 0
        threestar = 0
        twostar = 0
        onestar = 0
        valortotal = 0
        qtdreviews = len(reviews)
        
        for r in reviews:
            valor = r.rating
            valortotal += valor
            if valor == 1:
                onestar += 1
            elif valor == 2:
                twostar += 1
            elif valor == 3:
                threestar += 1   
            elif valor == 4:
                fourstar += 1
            elif valor == 5:
                fivestar += 1

        if qtdreviews ==0:
            qtdreviews = 1
        mediareviews = (valortotal)/qtdreviews  
        mediarating = (mediareviews)
        porcento1 = (onestar*100)/qtdreviews
        porcento2 = (twostar*100)/qtdreviews
        porcento3 = (threestar*100)/qtdreviews
        porcento4 = (fourstar*100)/qtdreviews
        porcento5 = (fivestar*100)/qtdreviews
                

        return render(request, 'pages/single.html', {'prod':produtoExibir, 'variacoes':variacoes, 'materiais':materiais, 'tags':tags, 'fotos':fotos, 'reviews':reviews, 'onestar':onestar, "twostar":twostar, "threestar":threestar, "fourstar":fourstar, "fivestar":fivestar, 'qtdreviews':(len(reviews)),'mediarating':mediarating, 'porcento1':porcento1,'porcento2':porcento2,'porcento3':porcento3,'porcento4':porcento4,'porcento5':porcento5})

    else:
        return render(request, 'pages/login.html', {'msg':'Por favor, efetue o login para avaliar um produto'})



