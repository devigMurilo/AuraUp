from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from apps.empresas.models import Follow
from apps.publicacoes.models import Publicacao

DASHBOARD_TEMPLATE = 'pages/dashboard.html'


@login_required
def dashboard_view(request):
    empresa = request.user.empresa

    # Seguidores por mês
    seguidores_por_mes = (
        Follow.objects.filter(empresa=empresa)
        .annotate(mes=TruncMonth('seguido_em'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    # Publicações por mês
    publicacoes_por_mes = (
        Publicacao.objects.filter(empresa=empresa)
        .annotate(mes=TruncMonth('criado_em'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    # Top 5 posts por curtidas
    top_posts = (
        empresa.publicacoes
        .annotate(num_curtidas=Count('curtidas'))
        .order_by('-num_curtidas')[:5]
    )

    # Dados para Chart.js (listas simples)
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
