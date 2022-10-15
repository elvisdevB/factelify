from django.contrib import admin
from.models import *

# Register your models here.


class AdminFactura(admin.ModelAdmin):
    list_display=["id","id_cliente","subtotal","total"]
    search_fields=["id"]
    class Meta:
        model=Factura


admin.site.register(Factura, AdminFactura) 

class AdminDetalle(admin.ModelAdmin):
    list_display = ['id_factura', 'id_producto','cantidad','subtotal']
    class Meta:
        model = DetalleFactura

admin.site.register(DetalleFactura, AdminDetalle) 