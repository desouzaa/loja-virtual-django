from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("process/", views.PaginaDePagamento, name="process"),
    path("failure/", views.PaymentFailureView, name="failure"),
    path("pending/", views.PaymentPendingView, name="pending"),
    path("success/", views.PaymentSuccessView, name="success"),
    path("webhook/", views.Payment_webhook, name="webhook"),
    path("pay/", views.PaymentPayView, name="pay"),
    path("pay2/", views.PaymentPay2View, name="pay2"),
    path("process_payment/", views.PaymentProcess, name="paymentProcess"),
    path("process_payment2/", views.Process_payment2, name="paymentProcess2")
]