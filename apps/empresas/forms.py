from django import forms
from .models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model  = Empresa
        fields = ['nome_fantasia', 'descricao', 'categoria', 'cidade', 'foto_perfil', 'contato']
        labels = {
            'nome_fantasia': 'Nome da empresa',
            'descricao':     'Descrição',
            'categoria':     'Categoria',
            'cidade':        'Cidade',
            'foto_perfil':   'Foto de perfil',
            'contato':       'Telefone / Site',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
