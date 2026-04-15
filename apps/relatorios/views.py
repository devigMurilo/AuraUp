from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from apps.empresas.models import Follow
from apps.publicacoes.models import Publicacao
from .utils import (
    calcular_periodo, calcular_kpis, gerar_grafico_seguidores,
    gerar_grafico_publicacoes, gerar_distribuicao_avaliacoes,
    gerar_top_5_posts
)

DASHBOARD_TEMPLATE = 'pages/dashboard.html'


@login_required
def dashboard_view(request):
    if not hasattr(request.user, 'empresa'):
        return redirect('minha_empresa')
    
    empresa = request.user.empresa

    seguidores_por_mes = (
        Follow.objects.filter(empresa=empresa)
        .annotate(mes=TruncMonth('seguido_em'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    publicacoes_por_mes = (
        Publicacao.objects.filter(empresa=empresa)
        .annotate(mes=TruncMonth('criado_em'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    top_posts = (
        empresa.publicacoes_empresa.all()
        .annotate(num_curtidas=Count('curtidas'))
        .order_by('-num_curtidas')[:5]
    )

    labels_seg  = [item['mes'].strftime('%b/%Y') for item in seguidores_por_mes]
    valores_seg = [item['total'] for item in seguidores_por_mes]
    labels_pub  = [item['mes'].strftime('%b/%Y') for item in publicacoes_por_mes]
    valores_pub = [item['total'] for item in publicacoes_por_mes]

    return render(request, DASHBOARD_TEMPLATE, {
        'empresa':       empresa,
        'top_posts':     top_posts,
        'labels_seg':    labels_seg,
        'valores_seg':   valores_seg,
        'labels_pub':    labels_pub,
        'valores_pub':   valores_pub,
    })


@login_required
def empresa_dashboard_view(request):
    if not hasattr(request.user, 'empresa'):
        return redirect('minha_empresa')
    
    empresa = request.user.empresa
    periodo = request.GET.get('periodo', '12m')
    
    kpis = calcular_kpis(empresa, periodo)
    
    grafico_seguidores = gerar_grafico_seguidores(empresa, periodo)
    grafico_publicacoes = gerar_grafico_publicacoes(empresa, periodo)
    grafico_avaliacoes = gerar_distribuicao_avaliacoes(empresa)
    top_posts = gerar_top_5_posts(empresa, periodo)
    
    publicacoes_recentes = empresa.publicacoes_empresa.all().order_by('-criado_em')[:10]
    avaliacoes_recentes = empresa.avaliacoes.all().order_by('-criado_em')[:10]
    seguidores_recentes = empresa.follows.all().order_by('-seguido_em')[:20]
    
    periodos = ['hoje', '7d', '30d', '3m', '12m']
    
    context = {
        'empresa': empresa,
        'periodo': periodo,
        'periodos': periodos,
        'kpis': kpis,
        'grafico_seguidores': grafico_seguidores,
        'grafico_publicacoes': grafico_publicacoes,
        'grafico_avaliacoes': grafico_avaliacoes,
        'top_posts': top_posts,
        'publicacoes_recentes': publicacoes_recentes,
        'avaliacoes_recentes': avaliacoes_recentes,
        'seguidores_recentes': seguidores_recentes,
    }
    
    return render(request, 'pages/empresa_dashboard.html', context)
