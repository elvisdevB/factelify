from django import forms
from django.db.models import fields
from app.cliente_proveedor.models.models import Cliente, Proveedor


class FormularioCliente(forms.ModelForm):
	class Meta:
		model = Cliente
		fields=["cedula","nombre","apellido","telefono","genero","direccion"]#lo que voy a representar en la parte grafica
		labels={
			"cedula":"Cedula",
			"nombre":"Nombre",
			"apellido":"Apellidos",
			"telefono":"Telefono",
			"genero":"Genero",
			"direccion":"Direccion",
		}
		widgets={
			'cedula':forms.TextInput(attrs={'class':'form-control','placeholder':'Cedula...','maxlength':'10'}),
			'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre...'}),
			'apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos...'}),
			'telefono':forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono...','maxlength':'10'}),
			'genero':forms.Select(attrs={'class':'form-control','placeholder':'Genero...'}),
			'direccion':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Direccion...'}),
		}

		
	def save(self, commit=True):
		data={}
		form = super()
		try:
			if form.is_valid():
				instance = form.save()
				data = instance.toJSON()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data



class FormularioProveedor(forms.ModelForm):
	class Meta:
		model = Proveedor
		fields = ["identificacion","nombre","telefono","direccion"]

		labels={
			"identificacion":"Nº Identificacion",
			"nombre":"Nombre",
			"telefono":"Telefono",
			"direccion":"Direccion",
		}

		widgets={
			'identificacion':forms.TextInput(attrs={'class':'form-control','type':"text",'placeholder':'Identificacion...','maxlength':'10'}),
			'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre...','onkeypress':'return sololetras(event)'}),
			'telefono':forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono...','maxlength':'10','onkeypress':'return solonumeros(event)'}),
			'direccion':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Direccion...'}),
		}
	
	def save(self, commit=True):
		data={}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data