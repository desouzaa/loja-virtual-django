from django.contrib import admin

from .models import ItemPedido, Pedido, Status
from payments.models import Payment


class ItemInline(admin.TabularInline):
    model = ItemPedido
    raw_id_fields = ["id_produto"]
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    can_delete = False
    readonnly_fields = {
        "email",
        "doc_number",
        "transaction_amount",
        "installments",
        "payment_method_id",
        "mercado_pago_id",
        "mercado_pago_status",
        "mercado_pago_status_detail",
        "modified",
    }

    ordering = ("-modified",)
    
    def has_add_permission(self, request, obj):
        return False


@admin.register(Pedido)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__","numero_pedido","id_cliente","id_endereco","paid", "status_pedido", "created","modified"]
    list_filter = ["paid", "created", "modified", "status_pedido"]
    search_fields = ["id_cliente"]
    inlines = [ItemInline, PaymentInline]

admin.site.register(Status)

