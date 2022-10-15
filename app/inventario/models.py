import json
from django.db import models
from django.forms.models import model_to_dict
from app.cliente_proveedor.models.models import Proveedor
from factelify.settings.base import STATIC_URL
from factelify.settings.development import MEDIA_URL


class Categoria(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['descripcion'] = self.descripcion
        return item



class Producto(models.Model):
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150,null=True)
    codigoPrincipal = models.CharField(max_length=10, null=True)
    codigoAuxiliar = models.CharField(max_length=10, null=True)
    descuento = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    precio = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)

    def __str__(self):
        string=self.codigoPrincipal
        return string
    
    
    def toJSON(self):
        item = model_to_dict(self)
        item['id_proveedor'] = self.id_proveedor.nombre
        item['id_categoria'] = self.id_categoria.nombre
        item['codigoAuxiliar'] = self.codigoAuxiliar
        item['codigoAuxiliar'] = self.codigoAuxiliar
        item['descuento'] = format(self.descuento,'.2f')
        item['precio'] = format(self.precio,'.2f')
        return item