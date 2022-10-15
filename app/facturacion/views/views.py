import json
from webbrowser import get

from django.db import transaction
from django.views.generic import *
from app.cliente_proveedor.forms import FormularioCliente
from app.facturacion.models import Factura, DetalleFactura
from app.inventario.models import Producto
from app.cliente_proveedor.models.models import Cliente
from app.facturacion.forms import *
from django.urls import reverse_lazy
from  django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
#Generar PDF
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import  get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
# Create your views here.

class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = "facturacion/listar_factura.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Factura.objects.all():
                    data.append(i.toJSON())
            elif action == "search_details_prod":
                data = []
                for i in DetalleFactura.objects.filter(id_factura=request.POST['id']):
                    data.append(i.toJSON())
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except  Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Lista de Ventas'
        context["entidad"] = "Facturas"
        context["create_url"] = reverse_lazy("facturacion:registrar_venta")
        context["list_url"] = reverse_lazy("facturacion:listar_venta")
        return context


class FacturaCreateView(LoginRequiredMixin,CreateView):
    model = Factura
    form_class = FormularioFactura
    template_name = "facturacion/registrar_venta.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action =request.POST['action']
            if action == 'search_productos':
                data = []
                productos = Producto.objects.filter(nombre__icontains = request.POST['term'])[0:10]
                for i in productos:
                    item = i.toJSON()
                    item['value'] =i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    factura = Factura()
                    factura.id_cliente_id = vents['id_cliente']
                    factura.subtotal = float(vents['subtotal'])
                    factura.iva = float(vents['iva'])
                    factura.total = float(vents['total'])
                    factura.fecha_emision = vents['fecha_emision']
                    factura.save()

                    for i in vents['productos']:
                        detalle = DetalleFactura()
                        detalle.id_producto_id = i['id']
                        detalle.id_factura_id = factura.id
                        detalle.cantidad = int(i['cantidad'])
                        detalle.subtotal = float(i['subtotal'])
                        detalle.save()
                    
                    data = {'id':factura.id}
                    print(data)          
            elif action == 'search_clientes':
                data = []
                term = request.POST['term']
                clients = Cliente.objects.filter(
                    Q(nombre__icontains=term) | Q(apellido__icontains=term) | Q(cedula__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.full_name()
                    data.append(item)
            elif action == 'create_client':
                formCli = FormularioCliente(request.POST)
                data = formCli.save()
            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formInfoT'] = FormularioFactura
        context["titulo"] = 'Realizar Ventas'
        context["entidad"] = "Facturacion"
        context['action'] = 'add'
        context['formCliente'] = FormularioCliente()
        return context

class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    template_name = "facturacion/eliminar_factura.html"
    success_url = reverse_lazy("facturacion:listar_venta")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Eliminando Venta'
        context["entidad"] = "Facturacion de Cliente"
        context["list_url"] = self.success_url
        #context["action"] = "add"
        return context


class GenerarFacturaVolante(LoginRequiredMixin, View):
    

    
    def get(self, request,*args, **kwargs):
        try:
            template = get_template("facturacion/facturaPdf.html")
            context = {
                'sale': Factura.objects.get(pk=self.kwargs['pk']),
                'comp':{'name':'ElvisSOFT', 'ruc':'099999999999','address':'Milagro Ecuador'},
                'icono':'{}{}'.format(settings.STATIC_URL,'img/avatar/avatar-1.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="resport.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )

            if pisaStatus.err:
                return HttpResponse("Error <pre>" + html +"</pre>")
            return response
        
        except:
            pass
        return HttpResponseRedirect(reverse_lazy("facturacion:listar_venta"))

        