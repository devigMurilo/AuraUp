from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.empresas.models import Empresa
from .models import Avaliacao
from .forms import AvaliacaoForm


@login_required
def avaliar_view(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        # Impede avaliar a própria empresa
        if hasattr(request.user, 'empresa') and request.user.empresa == empresa:
            messages.error(request, 'Você não pode avaliar sua própria empresa.')
            return redirect('perfil_empresa', pk=pk)

        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            av, criada = Avaliacao.objects.get_or_create(
                usuario=request.user,
                empresa=empresa,
                defaults={
                    'nota':       form.cleaned_data['nota'],
                    'comentario': form.cleaned_data['comentario'],
                }
            )
            if not criada:
                av.nota       = form.cleaned_data['nota']
                av.comentario = form.cleaned_data['comentario']
                av.save()
                messages.success(request, 'Avaliação atualizada!')
            else:
                messages.success(request, 'Avaliação enviada!')
    return redirect('perfil_empresa', pk=pk)
