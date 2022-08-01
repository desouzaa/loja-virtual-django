from django.contrib import admin
from .models import *

admin.site.register(Solicitacoes)
admin.site.register(Cupons)
admin.site.register(Tipo_solicitacao)
admin.site.register(Status_solicitacao)
admin.site.register(Newsletter)
admin.site.register(Cupon_cliente)