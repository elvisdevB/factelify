from django.shortcuts import render
from django.views.generic import *
from app.core.user.models import User
from app.core.user.forms import UserForm, UserProfileForm
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from datetime import datetime

# Create your views here.
class UseriaListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user/listUser.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except  Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Listado de Usuarios'
        context["entidad"] = "Usuarios"
        context["create_url"] = reverse_lazy("registrar_usuarios")
        context["list_url"] = reverse_lazy("listar_usuarios")
        return context

class RegistrarUser(LoginRequiredMixin,CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/createUser.html'


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context["titulo"] = 'Crear Usuario'
        context["entidad"] = "Usuario"
        context["action"] = "add"
        context["list_url"] = reverse_lazy("listar_usuarios")
        return context


class EditarUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/createUser.html'


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
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar Usuario'
        context["entidad"] = "Usuario"
        context["action"] = "edit"
        context["list_url"] = reverse_lazy("listar_usuarios")
        return context


class UsuarioDeleteView(LoginRequiredMixin, DeleteView):

    model = User
    template_name = "user/eliminarUser.html"
    success_url = reverse_lazy("listar_usuarios")

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
        context["titulo"] = 'Eliminando Usuario'
        context["entidad"] = "Usuario"
        context["list_url"] = reverse_lazy("listar_usuarios")
        #context["action"] = "add"
        return context


class GroupView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('principal'))

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profileEdit.html'


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar de Perfil'
        context["entidad"] = "Perfil"
        context["action"] = "edit"
        context["list_url"] = reverse_lazy("principal")
        return context

class UserChangePassword(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = "Ingrese su contraseña actual"
        form.fields['old_password'].widget.attrs['class'] = "form-control"
        form.fields['new_password1'].widget.attrs['placeholder'] = "Ingrese su nueva contraseña"
        form.fields['new_password1'].widget.attrs['class'] = "form-control"
        form.fields['new_password2'].widget.attrs['placeholder'] = "Repita su contraseña"
        form.fields['new_password2'].widget.attrs['class'] = "form-control"
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = "No ha ingresado ninguna opccion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar Contraseña'
        context["entidad"] = "Password"
        context["action"] = "edit"
        context["list_url"] = reverse_lazy("login")
        return context
