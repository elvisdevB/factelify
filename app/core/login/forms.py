from django import forms
from app.core.user.models import User

class RessetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese su username',
        'class':'form-control',
        'autocomplete':'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username = cleaned['username']).exists():
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('El usuario no existe')
            #raise forms.ValidationError("El usuario no existe")
        return cleaned
    
    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Ingrese una nueva contraseña',
        'class':'form-control',
        'autocomplete':'off'
    }))

    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repita su contraseña',
        'class':'form-control',
        'autocomplete':'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmpassword = cleaned['confirmpassword']
        if password != confirmpassword:
            self._errors['error'] = self._errors.get('Error', self.error_class())
            self._errors['error'].append('Las contraseñas deben ser iguales')
            #raise forms.ValidationError("El usuario no existe")
        return cleaned


