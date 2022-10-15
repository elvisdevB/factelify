
from multiprocessing import AuthenticationError
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.views import  LoginView
from django.views.generic import FormView, RedirectView
from django.urls import  reverse_lazy
from django.contrib.auth import logout
from app.core.login.forms import RessetPasswordForm, ChangePasswordForm
from factelify.settings import development
from factelify.settings.base import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from factelify.settings.development import DEBUG
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#Email librerias
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from factelify.settings import base
from app.core.user.models import User

# Create your views here.

class LoguinFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesion'
        return context



class LogoutFormView(RedirectView):
    pattern_name = LOGOUT_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class ResetPasswordView(FormView):
    form_class = RessetPasswordForm
    template_name = 'resetPassword.html'
    success_url = reverse_lazy(LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_pwd(self, user):
        data = {}
        try:

            URL = base.DOMAIN if not development.DEBUG else self.request.META['HTTP_HOST']

            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(base.EMAIL_HOST, base.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(base.EMAIL_HOST_USER, base.EMAIL_HOST_PASSWORD)

            email_to = user.email
            print(base.EMAIL_HOST_USER)
            mensaje = MIMEMultipart()
            mensaje['From'] = base.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'

            content = render_to_string('send_email.html', {
                'user': user,
                'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(base.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = RessetPasswordForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
            else:
                data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def form_valid(self, form):
        pass
        return HttpResponseRedirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        return context



class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'change_pass.html'
    success_url = reverse_lazy(LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
                
            else:
                data ['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambio  de Contraseña'
        return context