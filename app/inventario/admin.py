from django.contrib import admin

from.models import *

# Register your models here.


class AdminProducto(admin.ModelAdmin):

    list_display = ["id_proveedor","id_categoria","nombre","codigoPrincipal","codigoAuxiliar","descuento","precio"]
    class Meta:
        model=Producto


admin.site.register(Producto, AdminProducto) 

class AdminCategoria(admin.ModelAdmin):

    list_display = ["nombre","descripcion"]
    class Meta:
        model=Categoria