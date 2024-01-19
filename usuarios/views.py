from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não conferem')
            return redirect('cadastro')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect('cadastro')
        try:
            User.objects.create_user(
                username=username,
                password=senha
            )
            return redirect('login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do servidor!')
            return redirect('cadastro')
    else:
        return render(request, 'cadastro.html')


def logar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado com sucesso!')
            return redirect('/flashcard/novo_flashcard')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos!')
            return redirect('/usuarios/logar')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.add_message(request, constants.SUCCESS, 'Deslogado com sucesso!')
    return redirect('/usuarios/logar')
