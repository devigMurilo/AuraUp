from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CadastroForm, LoginForm, PerfilForm

CADASTRO_TEMPLATE = 'pages/cadastro.html'
LOGIN_TEMPLATE = 'pages/login.html'
PERFIL_TEMPLATE = 'pages/perfil_usuario.html'


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('/feed/')
    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Bem-vindo, {user.nome}!')
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
        messages.error(request, 'E-mail ou senha incorretos.')
    return render(request, LOGIN_TEMPLATE)


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def perfil_view(request):
    form = PerfilForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil atualizado!')
        return redirect('/perfil/')
    return render(request, PERFIL_TEMPLATE, {'form': form})
