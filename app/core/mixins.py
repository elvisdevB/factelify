from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from crum import get_current_request


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required,)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('principal')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()
        if 'group' in request.session:
            group = request.session['group']

            perms = self.get_perms()

            for p in perms: 
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'Usted no tiene permisos para ingresar a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'Usted no tiene permisos para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())
