from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from  django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  login_required
from django.views.decorators.csrf import csrf_exempt
from app.cliente_proveedor.models.models import Cliente, Proveedor
from app.cliente_proveedor.forms import FormularioCliente, FormularioProveedor
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


#Views de Cliente
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'cliente/cliente_listar.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except  Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Lista de Clientes'
        context["entidad"] = "Cliente"
        context["create_url"] = reverse_lazy("cliente_proveedor:cliente_registrar")
        context["list_url"] = reverse_lazy("cliente_proveedor:cliente_listar")
        return context

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = FormularioCliente
    template_name = "cliente/registrar_cliente.html"
    success_url = reverse_lazy("cliente_proveedor:cliente_listar")

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action =request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Crear Nuevo Cliente'
        context["entidad"] = "Cliente"
        context["action"] = "add"
        context["list_url"] = reverse_lazy("cliente_proveedor:cliente_listar")
        return context

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = FormularioCliente
    template_name = "cliente/registrar_cliente.html"
    success_url = reverse_lazy("cliente_proveedor:cliente_listar")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado ninguna accion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar Cliente'
        context["entidad"] = "Cliente"
        context["list_url"] = reverse_lazy("cliente_proveedor:cliente_listar")
        context["action"] = "edit"
        return context

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "cliente/delete_cliente.html"
    success_url = reverse_lazy("cliente_proveedor:cliente_listar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Eliminando Cliente'
        context["entidad"] = "Cliente"
        context["list_url"] = reverse_lazy("cliente_proveedor:cliente_listar")
        #context["action"] = "add"
        return context

#Views de Proveedor
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'proveedor/proveedor_listar.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except  Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Lista de Proveedor'
        context["entidad"] = "Proveedor"
        context["create_url"] = reverse_lazy("cliente_proveedor:proveedor_registrar")
        context["list_url"] = reverse_lazy("cliente_proveedor:proveedor_listar")
        return context

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = FormularioProveedor
    template_name = "proveedor/registrar_proveedor.html"
    success_url = reverse_lazy("cliente_proveedor:proveedor_listar")

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action =request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Crear Nuevo Proveedor'
        context["entidad"] = "Proveedor"
        context["action"] = "add"
        context["list_url"] = reverse_lazy("cliente_proveedor:proveedor_listar")
        return context

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = FormularioProveedor
    template_name = "proveedor/registrar_proveedor.html"
    success_url = reverse_lazy("cliente_proveedor:proveedor_listar")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado ninguna accion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar Proveedor'
        context["entidad"] = "Proveedor"
        context["list_url"] = reverse_lazy("cliente_proveedor:proveedor_listar")
        context["action"] = "edit"
        return context

class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = "proveedor/delete_proveedor.html"
    success_url = reverse_lazy("cliente_proveedor:proveedor_listar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Eliminar Proveedor'
        context["entidad"] = "Proveedor"
        context["list_url"] = reverse_lazy("cliente_proveedor:proveedor_listar")
        #context["action"] = "add"
        return context