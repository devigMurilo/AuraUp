from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empresa, Follow
from .forms import EmpresaForm

LISTA_TEMPLATE = 'pages/empresas.html'
PERFIL_TEMPLATE = 'pages/perfil_empresa.html'
MINHA_EMPRESA_TEMPLATE = 'pages/minha_empresa.html'


def lista_empresas_view(request):
    empresas  = Empresa.objects.all()
    categoria = request.GET.get('categoria')
    busca     = request.GET.get('busca')
    if categoria:
        empresas = empresas.filter(categoria=categoria)
    if busca:
        empresas = empresas.filter(nome_fantasia__icontains=busca)
    return render(request, LISTA_TEMPLATE, {
        'empresas':  empresas,
        'categoria': categoria,
        'busca':     busca,
    })


def perfil_empresa_view(request, pk):
    empresa    = get_object_or_404(Empresa, pk=pk)
    ja_segue   = False
    if request.user.is_authenticated:
        ja_segue = Follow.objects.filter(usuario=request.user, empresa=empresa).exists()
    NOTAS = [(i, '★' * i) for i in range(1, 6)]
    return render(request, PERFIL_TEMPLATE, {
        'empresa':  empresa,
        'ja_segue': ja_segue,
        'notas': NOTAS,
    })


@login_required
def minha_empresa_view(request):
    empresa = getattr(request.user, 'empresa', None)
    form    = EmpresaForm(request.POST or None, request.FILES or None, instance=empresa)
    if request.method == 'POST' and form.is_valid():
        emp = form.save(commit=False)
        emp.usuario = request.user
        emp.save()
        messages.success(request, 'Perfil da empresa atualizado!')
        return redirect('/minha-empresa/')
    return render(request, MINHA_EMPRESA_TEMPLATE, {'form': form, 'empresa': empresa})


@login_required
def follow_view(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    follow, criado = Follow.objects.get_or_create(usuario=request.user, empresa=empresa)
    if not criado:
        follow.delete()
        messages.info(request, f'Você deixou de seguir {empresa.nome_fantasia}.')
    else:
        messages.success(request, f'Você está seguindo {empresa.nome_fantasia}!')
    return redirect('perfil_empresa', pk=pk)


# Categorias disponíveis (usadas no template lista.html)
CATEGORIAS = [
    ('alimentacao', 'Alimentação'),
    ('moda',        'Moda e Vestuário'),
    ('servicos',    'Serviços'),
    ('saude',       'Saúde e Beleza'),
    ('educacao',    'Educação'),
    ('tecnologia',  'Tecnologia'),
    ('outros',      'Outros'),
]


def lista_empresas_view_v2(request):
    empresas  = Empresa.objects.all()
    categoria = request.GET.get('categoria')
    busca     = request.GET.get('busca')
    if categoria:
        empresas = empresas.filter(categoria=categoria)
    if busca:
        empresas = empresas.filter(nome_fantasia__icontains=busca)
    return render(request, LISTA_TEMPLATE, {
        'empresas':   empresas,
        'categoria':  categoria,
        'busca':      busca,
        'categorias': CATEGORIAS,
    })
