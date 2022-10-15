from django.contrib import admin
from.models.models import *

# Register your models here.


class AdminCliente(admin.ModelAdmin):
    list_display = ["cedula", "nombre", "apellido"]
    list_editable = ["nombre", "apellido"]
    list_filter = ["genero"]
    search_fields = ["cedula", "apellido"]

    class Meta:
        model = Cliente


admin.site.register(Cliente, AdminCliente) 


class AdminProveedor(admin.ModelAdmin):
    list_display = ["identificacion", "nombre"]
    list_editable = ["nombre"]
    list_filter = ["nombre"]
    search_fields = ["identificacion", "nombre"]

    class Meta:
        model = Proveedor


admin.site.register(Proveedor, AdminProveedor)