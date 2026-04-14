from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario


class CadastroForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput, label='Senha', min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar senha')

    class Meta:
        model  = Usuario
        fields = ['nome', 'email', 'tipo']
        labels = {'nome': 'Nome completo', 'email': 'E-mail', 'tipo': 'Tipo de conta'}

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail')


class PerfilForm(forms.ModelForm):
    class Meta:
        model  = Usuario
        fields = ['nome', 'email']
