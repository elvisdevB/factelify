from django.shortcuts import render, redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from app.inventario.models import Producto, Categoria
from app.cliente_proveedor.models.models import Proveedor
from app.inventario.forms import FormProducto, TestForm, FormCategoria
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.core.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = FormCategoria
    template_name = 'categoria_add.html'
    success_url = reverse_lazy('producto_registrar')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
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
        context["titulo"] = 'Crear Nueva Categoria'
        context["entidad"] = "Categoria"
        context["action"] = "add"
        context["list_url"] = reverse_lazy("categoria_listar")
        return context

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_listar.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except  Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Categorias Presentes en la Tienda'
        context["entidad"] = "Categoria"
        context["create_url"] = reverse_lazy("categoria_registrar")
        context["list_url"] = reverse_lazy("categoria_listar")
        return context

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = FormCategoria
    template_name = "categoria_add.html"
    success_url = reverse_lazy("categoria_listar")

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
        context["titulo"] = 'Editar Categoria'
        context["entidad"] = "Categoria"
        context["list_url"] = reverse_lazy("categoria_listar")
        context["action"] = "edit"
        return context

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = "categoria_delete.html"
    success_url = reverse_lazy("categoria_listar")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Eliminando Categoria'
        context["entidad"] = "Categorias"
        context["list_url"] = reverse_lazy("producto_listar")
        #context["action"] = "add"
        return context

class ProductoListView(ValidatePermissionRequiredMixin, LoginRequiredMixin,ListView):
    model = Producto
    template_name = 'productos_listar.html'
    permission_required= 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except  Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Lista de Productos'
        context["entidad"] = "Producto"
        context["create_url"] = reverse_lazy("producto_registrar")
        context["list_url"] = reverse_lazy("producto_listar")
        return context

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = FormProducto
    template_name = "productos_add.html"
    success_url = reverse_lazy("producto_listar")


    def post(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action'] 
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
        context["titulo"] = 'Crear Nuevo Producto'
        context["entidad"] = "Producto"
        context["action"] = "add"
        context["list_url"] = reverse_lazy("producto_listar")
        return context


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = FormProducto
    template_name = "productos_add.html"
    success_url = reverse_lazy("producto_listar")

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
        context["titulo"] = 'Editar Producto'
        context["entidad"] = "Producto"
        context["list_url"] = reverse_lazy("producto_listar")
        context["action"] = "edit"
        return context


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos_delete.html"
    success_url = reverse_lazy("producto_listar")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Eliminando Producto'
        context["entidad"] = "Producto"
        context["list_url"] = reverse_lazy("producto_listar")
        #context["action"] = "add"
        return context


class TestView(TemplateView):
    template_name = 'test.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_producto_id':
                data = [{'id':'' , 'text':'-----------'}]
                for i in Producto.objects.filter(id_proveedor_id = request.POST['id']):
                    data.append({'id':i.id, 'text':i.nombre, 'data':i.id_proveedor.toJSON()})
            elif action == 'autocomplete':
                data =[]
                for i in Proveedor.objects.filter(nombre__icontains = request.POST['term'])[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Aninados | Django'
        context['form'] = TestForm()
        return context