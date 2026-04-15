from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Count
from .models import Publicacao, Curtida, Comentario
from .forms import PublicacaoForm, ComentarioForm

FEED_TEMPLATE = 'pages/feed.html'
DETALHE_TEMPLATE = 'pages/detalhe_publicacao.html'
CRIAR_TEMPLATE = 'pages/criar_publicacao.html'


def feed_view(request):
    publicacoes = Publicacao.objects.select_related('empresa', 'usuario').all()
    categoria   = request.GET.get('categoria')
    cidade      = request.GET.get('cidade')
    if categoria:
        publicacoes = publicacoes.filter(empresa__categoria=categoria)
    if cidade:
        publicacoes = publicacoes.filter(empresa__cidade__icontains=cidade)
    
    # Get trending posts (most liked)
    trending = Publicacao.objects.select_related('empresa', 'usuario').annotate(
        total_likes=Count('curtidas')
    ).order_by('-total_likes')[:5]
    
    return render(request, FEED_TEMPLATE, {
        'publicacoes': publicacoes,
        'trending': trending,
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
        
        # Logic: if user has a company, publish as company
        if hasattr(request.user, 'empresa') and request.user.empresa:
            pub.empresa = request.user.empresa
        else:
            pub.usuario = request.user
        
        pub.save()
        messages.success(request, 'Publication created!')
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
    publicacao = get_object_or_404(Publicacao, pk=pk)
    
    # Check if current user is the author (either usuario or empresa owner)
    is_author = publicacao.usuario == request.user or (hasattr(request.user, 'empresa') and publicacao.empresa == request.user.empresa)
    
    if not is_author:
        return HttpResponseForbidden('You cannot delete this publication.')
    
    publicacao.delete()
    messages.success(request, 'Publication deleted.')
    return redirect('/feed/')
