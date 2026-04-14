from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Publicacao, Curtida, Comentario
from .forms import PublicacaoForm, ComentarioForm

FEED_TEMPLATE = 'pages/feed.html'
DETALHE_TEMPLATE = 'pages/detalhe_publicacao.html'
CRIAR_TEMPLATE = 'pages/criar_publicacao.html'


def feed_view(request):
    publicacoes = Publicacao.objects.select_related('empresa').all()
    categoria   = request.GET.get('categoria')
    cidade      = request.GET.get('cidade')
    if categoria:
        publicacoes = publicacoes.filter(empresa__categoria=categoria)
    if cidade:
        publicacoes = publicacoes.filter(empresa__cidade__icontains=cidade)
    return render(request, FEED_TEMPLATE, {
        'publicacoes': publicacoes,
        'categoria':   categoria,
        'cidade':      cidade,
        'form_comentario': ComentarioForm(),
    })


def detalhe_publicacao_view(request, pk):
    publicacao = get_object_or_404(Publicacao, pk=pk)
    form       = ComentarioForm(request.POST or None)
    if request.method == 'POST' and request.user.is_authenticated:
        if form.is_valid():
            c = form.save(commit=False)
            c.usuario    = request.user
            c.publicacao = publicacao
            c.save()
            return redirect('detalhe_publicacao', pk=pk)
    return render(request, DETALHE_TEMPLATE, {
        'publicacao': publicacao,
        'form':       form,
    })


@login_required
def criar_publicacao_view(request):
    form = PublicacaoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        pub = form.save(commit=False)
        pub.empresa = request.user.empresa
        pub.save()
        messages.success(request, 'Publicação criada!')
        return redirect('/feed/')
    return render(request, CRIAR_TEMPLATE, {'form': form})


@login_required
def curtir_view(request, pk):
    publicacao = get_object_or_404(Publicacao, pk=pk)
    curtida, criada = Curtida.objects.get_or_create(usuario=request.user, publicacao=publicacao)
    if not criada:
        curtida.delete()
    return redirect(request.META.get('HTTP_REFERER', '/feed/'))


@login_required
def excluir_publicacao_view(request, pk):
    publicacao = get_object_or_404(Publicacao, pk=pk, empresa=request.user.empresa)
    publicacao.delete()
    messages.success(request, 'Publicação excluída.')
    return redirect('/feed/')
