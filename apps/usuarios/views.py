from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CadastroForm, LoginForm, PerfilForm
from .models import Usuario, FollowUsuario

CADASTRO_TEMPLATE = 'pages/cadastro.html'
LOGIN_TEMPLATE = 'pages/login.html'
MEU_PERFIL_TEMPLATE = 'pages/perfil_usuario.html'
PERFIL_USUARIO_TEMPLATE = 'pages/view_perfil_usuario.html'


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('/feed/')
    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.nome}!')
        return redirect('/feed/')
    return render(request, CADASTRO_TEMPLATE, {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/feed/')
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user     = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/feed/'))
        messages.error(request, 'Email or password incorrect.')
    return render(request, LOGIN_TEMPLATE)


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def perfil_view(request):
    form = PerfilForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated!')
        return redirect('/perfil/')
    return render(request, MEU_PERFIL_TEMPLATE, {'form': form})


def perfil_usuario_view(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    publicacoes = usuario.publicacoes_usuario.all()
    
    # Check if current user follows this usuario
    esta_seguindo = False
    if request.user.is_authenticated:
        esta_seguindo = FollowUsuario.objects.filter(
            usuario=request.user,
            usuario_seguido=usuario
        ).exists()
    
    context = {
        'usuario': usuario,
        'publicacoes': publicacoes,
        'esta_seguindo': esta_seguindo,
        'total_seguidores': usuario.seguidores.count(),
        'total_seguindo': usuario.seguindo_usuarios.count(),
    }
    return render(request, PERFIL_USUARIO_TEMPLATE, context)


@login_required
def follow_usuario_view(request, pk):
    usuario_alvo = get_object_or_404(Usuario, pk=pk)
    
    if usuario_alvo == request.user:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('/feed/')
    
    follow, criado = FollowUsuario.objects.get_or_create(
        usuario=request.user,
        usuario_seguido=usuario_alvo
    )
    
    if not criado:
        follow.delete()
        messages.info(request, f'You unfollowed {usuario_alvo.nome}.')
    else:
        messages.success(request, f'You are now following {usuario_alvo.nome}!')
    
    return redirect('perfil_usuario', pk=usuario_alvo.pk)
