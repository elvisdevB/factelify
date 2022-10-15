from django.db import models
from django.forms.models import model_to_dict

# Create your models here.


class Cliente(models.Model):
    listaGenero=(
        ('femenino','Femenino'),
        ('masculino','Masculino')
    )
    # id_cliente=models.AutoField(primary_key=True) este se genera automáticamente
    cedula=models.CharField(max_length=15,unique=True, null=False)
    nombre=models.CharField(max_length=50,null=False)
    apellido=models.CharField(max_length=50,null=False)
    telefono=models.CharField(max_length=10,null=False)
    genero=models.CharField(max_length=15,choices=listaGenero, default='Masculino',null=False)
    direccion=models.TextField(max_length=250)


    def full_name(self):
        return '{} {}, DNI: {}'.format(self.nombre, self.apellido, self.cedula)

    def __str__(self):
        return self.full_name()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cedula'] = self.cedula
        item['nombre'] = self.nombre
        item['apellido'] = self.apellido
        item['telefono'] = self.telefono
        item['genero'] = self.genero
        item['direccion'] = self.direccion
        item['full_name'] = self.full_name()
        return item

    



class Proveedor(models.Model):
    # id_proveedor=models.AutoField(primary_key=True)
    identificacion=models.CharField(max_length=10,unique=True, null=False)
    nombre=models.CharField(max_length=50,null=False)
    telefono=models.CharField(max_length=10,null=False)
    direccion=models.TextField(max_length=250)

    def NombreCompleto(self):
        cadena="{2}{3}"
        return cadena.format(self.identificacion,self.nombre)

    def __str__(self):
        string=str(self.identificacion)+' '+str(self.nombre)
        return string
    
    def toJSON(self):
        item = model_to_dict(self)
        item['identificacion'] = self.identificacion
        item['nombre'] = self.nombre
        item['telefono'] = self.telefono
        item['direccion'] = self.direccion
        return item

