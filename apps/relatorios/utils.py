from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
import json


def calcular_periodo(periodo_str):
    hoje = timezone.now().date()
    if periodo_str == 'hoje':
        return hoje, hoje
    elif periodo_str == '7d':
        return hoje - timedelta(days=7), hoje
    elif periodo_str == '30d':
        return hoje - timedelta(days=30), hoje
    elif periodo_str == '3m':
        return hoje - timedelta(days=90), hoje
    else:
        return hoje - timedelta(days=365), hoje


def calcular_mudanca(valor_atual, valor_anterior):
    if valor_anterior == 0:
        return valor_atual if valor_atual > 0 else 0
    return valor_atual - valor_anterior


def gerar_grafico_seguidores(empresa, periodo_str='12m'):
    data_inicio, data_fim = calcular_periodo(periodo_str)
    seguidores = empresa.follows.filter(
        seguido_em__date__range=[data_inicio, data_fim]
    ).annotate(
        data=TruncDate('seguido_em')
    ).values('data').annotate(
        count=Count('id')
    ).order_by('data')
    
    dados = []
    labels = []
    total_acumulativo = 0
    for item in seguidores:
        total_acumulativo += item['count']
        dados.append(total_acumulativo)
        labels.append(item['data'].strftime('%d/%m'))
    
    return {'labels': json.dumps(labels), 'dados': json.dumps(dados)}


def gerar_grafico_publicacoes(empresa, periodo_str='12m'):
    data_inicio, data_fim = calcular_periodo(periodo_str)
    publicacoes = empresa.publicacoes_empresa.filter(
        criado_em__date__range=[data_inicio, data_fim]
    ).annotate(
        data=TruncDate('criado_em')
    ).values('data').annotate(
        count=Count('id')
    ).order_by('data')
    
    dados = []
    labels = []
    for item in publicacoes:
        dados.append(item['count'])
        labels.append(item['data'].strftime('%d/%m'))
    
    return {'labels': json.dumps(labels), 'dados': json.dumps(dados)}


def gerar_distribuicao_avaliacoes(empresa):
    labels = ['5 Estrelas', '4 Estrelas', '3 Estrelas', '2 Estrelas', '1 Estrela']
    dados = [
        empresa.avaliacoes.filter(nota=5).count(),
        empresa.avaliacoes.filter(nota=4).count(),
        empresa.avaliacoes.filter(nota=3).count(),
        empresa.avaliacoes.filter(nota=2).count(),
        empresa.avaliacoes.filter(nota=1).count(),
    ]
    cores = ['#00b96b', '#faad14', '#fadb14', '#ff7a45', '#ff4d4f']
    return {'labels': json.dumps(labels), 'dados': json.dumps(dados), 'cores': json.dumps(cores)}


def gerar_top_5_posts(empresa, periodo_str='12m'):
    data_inicio, data_fim = calcular_periodo(periodo_str)
    posts = empresa.publicacoes_empresa.filter(
        criado_em__date__range=[data_inicio, data_fim]
    ).annotate(
        curtidas_count=Count('curtidas', distinct=True),
        comentarios_count=Count('comentarios', distinct=True)
    ).order_by('-curtidas_count')[:5]
    
    titulos = [p.titulo[:30] + '...' if len(p.titulo) > 30 else p.titulo for p in posts]
    engajamentos = [p.curtidas_count + p.comentarios_count for p in posts]
    
    return {'titulos': json.dumps(titulos), 'engajamentos': json.dumps(engajamentos)}


def calcular_kpis(empresa, periodo_str='12m'):
    data_inicio, data_fim = calcular_periodo(periodo_str)
    
    total_publicacoes = empresa.publicacoes_empresa.count()
    total_seguidores = empresa.total_seguidores
    media_avaliacoes = empresa.media_avaliacoes
    total_avaliacoes = empresa.avaliacoes.count()
    
    publicacoes_periodo = empresa.publicacoes_empresa.filter(
        criado_em__date__range=[data_inicio, data_fim]
    )
    
    curtidas_periodo = publicacoes_periodo.aggregate(
        total=Count('curtidas', distinct=True)
    )['total'] or 0
    
    comentarios_periodo = publicacoes_periodo.aggregate(
        total=Count('comentarios', distinct=True)
    )['total'] or 0
    
    seguidores_periodo = empresa.follows.filter(
        seguido_em__date__range=[data_inicio, data_fim]
    ).count()
    
    dias_periodo = (data_fim - data_inicio).days + 1
    data_inicio_anterior = data_inicio - timedelta(days=dias_periodo)
    data_fim_anterior = data_inicio - timedelta(days=1)
    
    publicacoes_anterior = empresa.publicacoes_empresa.filter(
        criado_em__date__range=[data_inicio_anterior, data_fim_anterior]
    ).count()
    
    seguidores_anterior = empresa.follows.filter(
        seguido_em__date__range=[data_inicio_anterior, data_fim_anterior]
    ).count()
    
    mudanca_publicacoes = calcular_mudanca(publicacoes_periodo.count(), publicacoes_anterior)
    mudanca_seguidores = calcular_mudanca(seguidores_periodo, seguidores_anterior)
    
    return {
        'total_publicacoes': total_publicacoes,
        'total_seguidores': total_seguidores,
        'media_avaliacoes': media_avaliacoes,
        'total_avaliacoes': total_avaliacoes,
        'total_curtidas': curtidas_periodo,
        'total_comentarios': comentarios_periodo,
        'mudanca_publicacoes': mudanca_publicacoes,
        'mudanca_seguidores': mudanca_seguidores,
        'periodo': periodo_str,
    }
