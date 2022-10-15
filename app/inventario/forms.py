from cProfile import label
from dataclasses import field
from pyexpat import model
from django import forms
from app.inventario.models import Producto
from app.cliente_proveedor.models.models import *
from app.inventario.models import Producto, Categoria

class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion']

        label = {
            'nombre':'Nombre de la Categoria',
            'descripion':'Describir la Categoria'
        }

        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la Categoria'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':"10", 'cols':"50"})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
 


class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["id_proveedor","id_categoria","nombre","codigoPrincipal","codigoAuxiliar","descuento","precio"]

        labels = {
            "id_proveedor":"Proveedor del Producto",
            "id_categoria":"Categoria del Producto",
            "nombre":"Nombre del Producto",
            "codigoPrincipal":"Ingrese el Codigo Principal del Producto",
            "codigoAuxiliar":"Codigo auxiliar del Producto",
            "descuento":"Ingrese el Descuento del Producto",
            "precio":"Precio del Producto",
        }

        widgets = {
            'id_proveedor':forms.Select(attrs={'class':'form-control','placeholder':'Selecione Proveedor del Producto'}),
            'id_categoria':forms.Select(attrs={'class':'form-control','placeholder':'Selecione Categoria del Producto'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del Producto'}),
            'codigoPrincipal':forms.TextInput(attrs={'class':'form-control','placeholder':'Codigo del Producto...','onkeypress':'return sololetras(event)'}),
            'codigoAuxiliar':forms.TextInput(attrs={'class':'form-control','placeholder':'Codigo del Producto...','onkeypress':'return sololetras(event)'}),
			'descuento':forms.NumberInput(attrs={'class':'form-control'}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
        }
    

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
 


class TestForm(forms.Form):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    productos = forms.ModelChoiceField(queryset=Producto.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'style': 'width: 100%'
    # }))
    
    search = forms.ModelChoiceField(queryset=Producto.objects.none(), widget=forms.Select(attrs={
         'class': 'form-control select2',
         'style': 'width: 100%'
    }))
