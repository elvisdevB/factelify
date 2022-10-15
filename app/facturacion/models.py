from django.db import models
from app.inventario.models import Producto
from app.cliente_proveedor.models.models import Cliente
from datetime import datetime
from django.forms.models import model_to_dict

# Create your models here.


class Factura(models.Model):
    # id_factura=models.AutoField(primary_key=True) esta ya se genera automáticamente no es necesario agregar
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField( max_digits=10, decimal_places=2)
    fecha_emision = models.DateField(default = datetime.now)

    def __str__(self):
        return self.id_cliente.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['id_cliente'] = self.id_cliente.cedula
        item['subtotal'] = format(self.subtotal,'.2f')
        item['iva'] = format(self.iva,'.2f')
        item['total'] = format(self.total,'.2f')
        item['fecha_emision'] = self.fecha_emision
        return item


class DetalleFactura(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id_producto.codigoPrincipal

    def toJSON(self):
        item = model_to_dict(self, exclude=['id_factura'])
        item['id_producto'] = self.id_producto.toJSON()
        item['cantidad'] = format(self.cantidad,'.2f')
        item['subtotal'] = format(self.subtotal,'.2f')
        return item