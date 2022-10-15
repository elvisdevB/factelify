from datetime import datetime
from django import forms
from django.forms.widgets import Select
from app.cliente_proveedor.models.models import Cliente
from app.facturacion.models import Factura


class FormularioFactura(forms.ModelForm):


	class Meta:
		model = Factura
		fields=[
			"id_cliente",
			"subtotal",
			"iva",
			"total",
			"fecha_emision",
		]
		labels={
			"id_cliente":"Cliente",
			"subtotal":"Subtotal",
            "iva":"IVA",
            "total":"Total a Pagar",
			"fecha_emision":"Fecha"

		}
		widgets={
			'id_cliente':forms.Select(attrs={'class':'form-select select2'}),
			'fecha_emision':forms.DateInput(format="%Y-%m-%d",
												attrs={
													'value':datetime.now().strftime('%Y-%m-%d'),
													'autocomplete':'off',
													'class':'form-control datetimepicker-input',
													'id':'date_joined',
													'data-target':'#date_joined',
													'data-toggle':'datetimepicker'}),
			'subtotal':forms.NumberInput(attrs={
				'class':'form-control',
				'readonly':True
			}),
			'iva':forms.NumberInput(attrs={'class':'form-control','readonly':True}),
			'total':forms.NumberInput(attrs={
				'class':'form-control',
				'readonly':True
			})
		}
