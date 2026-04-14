from django import forms
from .models import Publicacao, Comentario


class PublicacaoForm(forms.ModelForm):
    class Meta:
        model  = Publicacao
        fields = ['titulo', 'conteudo', 'imagem']
        labels = {'titulo': 'Título', 'conteudo': 'Conteúdo', 'imagem': 'Imagem (opcional)'}
        widgets = {'conteudo': forms.Textarea(attrs={'rows': 4})}


class ComentarioForm(forms.ModelForm):
    class Meta:
        model  = Comentario
        fields = ['texto']
        labels = {'texto': ''}
        widgets = {'texto': forms.TextInput(attrs={'placeholder': 'Escreva um comentário...'})}
