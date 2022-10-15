from cProfile import label
from dataclasses import field
from pyexpat import model
from re import A
from django import forms
from app.core.user.models import User
from app.cliente_proveedor.models.models import *


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','img','groups']


        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su nombre'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su apellido'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su email'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su nombre de usuario'}),
            'password':forms.PasswordInput(render_value = True, attrs={'class':'form-control','placeholder':'Ingrese su contraseña'}),
            'img':forms.FileInput(attrs={'class':'form-control','placeholder':'Ingrese su Foto'}),
            'groups':forms.SelectMultiple(attrs={
                'class':'form-control select2',
                'style':'width: 100%',
                'multiple':'multiple'
            })
        }

        exclude = {'user_permissions','date_joined'}
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():

                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk = u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)

            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','img']


        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su nombre'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su apellido'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su email'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su nombre de usuario'}),
            'password':forms.PasswordInput(render_value = True, attrs={'class':'form-control','placeholder':'Ingrese su contraseña'}),
            'img':forms.FileInput(attrs={'class':'form-control','placeholder':'Ingrese su Foto'}),
        }

        exclude = {'user_permissions','date_joined','groups'}
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():

                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk = u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()

            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


