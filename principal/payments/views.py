import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import mercadopago
from pedidos.models import Pedido, Status
from produtos.models import Status_Produto
from .models import Payment

#redireciona para pagina de pagamento
@login_required   
def PaginaDePagamento(request):

    pay_method =  request.session.get("pay_method")
    order_id = request.session.get("order_id") #pega da sessao qual o pedido 
    order = get_object_or_404(Pedido, numero_pedido=order_id) #pesquisa o pedido no banco de dados
    transaction_amount = order.get_preco_total()+order.frete #pega o valor total do pedido
    publishable_key = settings.MERCADO_PAGO_PUBLIC_KEY #seta a chave publica para a pagina
    
    
    if pay_method == '1':
         return render(request, 'pages/payment_form.html', {'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key}) #redireciona com os dados

    elif pay_method == '2':
        
         return render(request, 'pages/payment_form2.html', {'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key}) #redireciona com os dados
    
    else:

        return render(request, 'pages/payment_form.html', {'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key}) #redireciona com os dados

#faz o processamento do pagamento
@login_required   
@require_POST
def PaymentProcess(request):

    valorConferir = request.POST.get("transactionAmount") #pega o valor total do pedido do formulario
    order_id = request.session.get("order_id") #pega o pedido da sessao
    order = get_object_or_404(Pedido, numero_pedido = order_id) #pega o pedido no banco de dados
    transaction_amount = order.get_preco_total()+order.frete #consulta o valor total do pedido no banco de dados
    publishable_key = settings.MERCADO_PAGO_PUBLIC_KEY #seta a chave publica para a pagina
       
    if float(valorConferir) != float(transaction_amount): #se os valores forem diferentes... redireciona para pagina anterior e recusa o processamento
        return render(request, 'pages/payment_form.html' ,{'msg':'Algum erro ocorreu durante o processamento, tente novamente', 'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key})

    mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    payment_data = {
    "transaction_amount": float(request.POST.get("transactionAmount")),
    "token": request.POST.get("token"),
    "description": order.get_description(),
    "installments": int(request.POST.get("installments")),
    "payment_method_id": request.POST.get("paymentMethodId"),
    "payer": {
        "email": request.POST.get("email"),
        "identification": {
            "type": request.POST.get("docType"), 
            "number": request.POST.get("docNumber")
                }
            }
        }


    payment = mp.payment().create(payment_data)
    
    
    if payment["status"] == 201:
        
        mercado_pago_id = payment["response"]["id"]
        
        mercado_pago_status_detail = payment["response"]["status_detail"]
        
        mercado_pago_status = payment["response"]["status"]
        

        pagamento = Payment.objects.create(order=order, transaction_amount=valorConferir, installments=int(request.POST.get("installments")), payment_method_id=request.POST.get("paymentMethodId"), email=request.POST.get("email"), doc_number=request.POST.get("docNumber"), mercado_pago_id=mercado_pago_id, mercado_pago_status_detail=mercado_pago_status_detail, mercado_pago_status=mercado_pago_status)

        pagamento.save()

        redirect_url = "payments:failure"

        if payment["response"]["status"] == "approved":
            Pedido.objects.filter(numero_pedido=order_id).update(paid=True)
            stat = Status.objects.get(id_status = 7)
            Pedido.objects.filter(numero_pedido=order_id).update(status_pedido=stat)
        
            redirect_url = "payments:success"     
              
        if payment["response"]["status"] == "in_process":
            stat = Status.objects.get(id_status = 11)
            Pedido.objects.filter(numero_pedido=order_id).update(status_pedido=stat)
            redirect_url = "payments:pending"

        if payment["response"]["status"] == "rejected":
            stat = Status.objects.get(id_status = 12)
            Pedido.objects.filter(numero_pedido=order_id).update(status_pedido=stat)
              

        if payment["response"]["status"] and payment["response"]["status"] != "rejected":
            del request.session["order_id"]
            del request.session["pay_method"]
            

        return redirect(redirect_url)
    return redirect('payments:failure')

#faz o processamento do pagamento
@login_required   
@require_POST
def Process_payment2(request):

    valorConferir = request.POST.get("transactionAmount") #pega o valor total do pedido do formulario
    order_id = request.session.get("order_id") #pega o pedido da sessao
    order = get_object_or_404(Pedido, numero_pedido = order_id) #pega o pedido no banco de dados
    transaction_amount = order.get_preco_total()+order.frete #consulta o valor total do pedido no banco de dados
    publishable_key = settings.MERCADO_PAGO_PUBLIC_KEY #seta a chave publica para a pagina
       
    if float(valorConferir) != float(transaction_amount): #se os valores forem diferentes... redireciona para pagina anterior e recusa o processamento
        return render(request, 'pages/payment_form2.html' ,{'msg':'Algum erro ocorreu durante o processamento, tente novamente', 'order':order, 'transaction_amount':transaction_amount, 'publishable_key':publishable_key})

    mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    payment_data = {
    "transaction_amount": transaction_amount,
    "description": order.get_description(),
    "payment_method_id": request.POST.get('paymentMethod'),
    "payer": {
        "email":  request.POST.get('payerEmail'),
        "first_name":  request.POST.get('payerFirstName'),
        "last_name":  request.POST.get('payerLastName'),
        "identification": {
            "type":  request.POST.get('docType'),
            "number":  request.POST.get('docNumber')
        },
        "address": {
            "zip_code": "06233-200",
            "street_name": "Av. das Nações Unidas",
            "street_number": "3003",
            "neighborhood": "Bonfim",
            "city": "Osasco",
            "federal_unit": "SP"
                }
            }
        }
    
    payment = mp.payment().create(payment_data)
    

    if payment["status"] == 201:
                
        mercado_pago_id = payment["response"]["id"]
        
        mercado_pago_status_detail = payment["response"]["status_detail"]
        
        mercado_pago_status = payment["response"]["status"]
        

        pagamento = Payment.objects.create(order=order, transaction_amount=transaction_amount, installments=int(1), payment_method_id=request.POST.get("paymentMethod"), email=request.POST.get("payerEmail"), doc_number=request.POST.get("docNumber"), mercado_pago_id=mercado_pago_id, mercado_pago_status_detail=mercado_pago_status_detail, mercado_pago_status=mercado_pago_status)

        pagamento.save()
                     
        if mercado_pago_status == "approved":
            Pedido.objects.filter(numero_pedido=order_id).update(paid=True)
            stat = Status.objects.get(id_status = 7)
            Pedido.objects.filter(numero_pedido=order_id).update(status_pedido=stat)
            del request.session["order_id"]
            del request.session["pay_method"]
            redirect_url = "pages/success.html"    
              
        if mercado_pago_status == "pending":
            redirect_url = "pages/pay.html"
            stat = Status.objects.get(id_status = 1)
            Pedido.objects.filter(numero_pedido=order_id).update(status_pedido=stat)
            


            if payment["response"]["payment_method_id"] == "pix":
                qrbase64 = payment["response"]["point_of_interaction"]["transaction_data"]["qr_code_base64"]
                imgg = f'data:image/jpeg;base64,{qrbase64}'
                qr_code = payment["response"]["point_of_interaction"]["transaction_data"]["qr_code"] 
                del request.session["order_id"]
                del request.session["pay_method"]
                Payment.objects.filter(id=pagamento.id).update(img=imgg, qr=qr_code)

                return render(request, redirect_url, {'img':imgg, 'qr_code':qr_code})
               

            elif payment["response"]["payment_method_id"] == "pec":
                redirect_url = payment["response"]["transaction_details"]["external_resource_url"]
                Payment.objects.filter(id=pagamento.id).update(link=redirect_url)
                

            elif payment["response"]["payment_method_id"] == "bolbradesco":
                redirect_url = payment["response"]["transaction_details"]["external_resource_url"]
                Payment.objects.filter(id=pagamento.id).update(link=redirect_url)

            
            del request.session["order_id"]
            del request.session["pay_method"]


            return render(request, "pages/pay2.html", {"redirect_url":redirect_url})

        if mercado_pago_status and mercado_pago_status != "rejected":
            del request.session["order_id"]
            del request.session["pay_method"]
        
            
        return render(request, "pages/failure.html")
    
    del request.session["order_id"]
    del request.session["pay_method"]
    return render(request, "pages/failure.html")

@login_required
def PaymentFailureView(request):
    template_name = "pages/failure.html"
    return render(request, template_name)

@login_required
def PaymentPendingView(request):
    template_name = "pages/pending.html"
    return render(request, template_name)

@login_required
def PaymentPayView(request):
    template_name = "pages/pay.html"
    return render(request, template_name)    

@login_required
def PaymentPay2View(request):
    template_name = "pages/pay2.html"
    return render(request, template_name)        

@login_required
def PaymentSuccessView(request):
    template_name = "pages/success.html"
    return render(request, template_name)

@csrf_exempt
@require_POST
def Payment_webhook(request): #metodo da view que recebe mensagens do mercado livre de atualizações sobre pagamento e faz o processamento no banco de dados

    datageral = json.loads(request.body) #recebe o json do mercado pago
    action = datageral.get('action') #ação
    data = datageral.get('data') # dados
           
    mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN) #define o SDK do mercado pago
    
    if action == "payment.updated": #se a ação for de atualização do pagamento ira...
        mercado_pago_id = data.get('id') #pegar o id do pagamento
        
        payment = Payment.objects.get(mercado_pago_id=mercado_pago_id) #pesquisar no banco de dados o pagamento usando o id
        order = payment.order #buscar o pedido que possui esse pagamento
        order_id = order.numero_pedido #pega o número desse pedido
        payment_mp = mp.payment().get(mercado_pago_id) #busca no mercado pago os dados do pagamento

        Payment.objects.filter(order=order).update(mercado_pago_status = payment_mp["response"]["status"], mercado_pago_status_detail = payment_mp["response"]["status_detail"]) #atualiza no banco de dados

        if payment_mp["response"]["status"] == "approved": # se o pagamento for aprovado irá colocar no pedido
            stat = Status.objects.get(id_status=7)
            Pedido.objects.filter(numero_pedido=order_id).update(paid=True, status_pedido = stat)

        elif payment_mp["response"]["status"] == "rejected":   
            stat = Status.objects.get(id_status=12)
            Pedido.objects.filter(numero_pedido=order_id).update(paid=False, status_pedido = stat)

        elif payment_mp["response"]["status"] == "cancelled":   
            stat = Status.objects.get(id_status=2)
            Pedido.objects.filter(numero_pedido=order_id).update(paid=False, status_pedido = stat)

        elif payment_mp["response"]["status"] == "refunded":   
            stat = Status.objects.get(id_status=13)
            Pedido.objects.filter(numero_pedido=order_id).update(paid=False, status_pedido = stat)

        else:
            stat = Status.objects.get(id_status=1)
            Pedido.objects.filter(numero_pedido=order_id).update(paid=False, status_pedido = stat)
     

    return JsonResponse({})
