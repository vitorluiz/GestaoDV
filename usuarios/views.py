from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256
from django.contrib import messages

def login(request):
    messages.add_message(request, constants.SUCCESS, "Seja bem vindo!!")
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')
    telefone = request.POST.get('telefone')

    if len(nome.strip()) == 0:
        messages.add_message(request,
                             constants.WARNING,
                             "E-mail ou Senha, não pode ser vázio!!")
        return redirect('/auth/cadastro/')
    if len(email.strip()) == 0:
        messages.add_message(request,
                             constants.WARNING,
                             "E-mail ou Senha, não pode ser vázio!!")        
        return redirect('/auth/cadastro/')
    if len(senha) < 8:
        messages.add_message(request, constants.WARNING, "A senha, deve ser maior que 8 caracteres!!")
        return redirect('/auth/cadastro/',)
    usuario = Usuario.objects.filter(email=email)

    if len(usuario) > 0:
        messages.add_message(request, constants.WARNING, "Usuário já cadastrado!!")
        return redirect('/auth/cadastro/')
    try:

        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome=nome,
                        senha=senha,
                        email=email,
                        telefone=telefone)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, "Cadastro realizado com Sucesso!")
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, constants.ERROR, "Erro interno do sistema!!")
        return redirect('/auth/cadastro/')
    

def valida_login(request):
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    senha = sha256(senha.encode()).hexdigest() 
    usuario = Usuario.objects.filter(email=email).filter(senha=senha)

    if len(usuario) == 0:
        messages.add_message(request, constants.WARNING, "E-mail ou Senha, inválido!!")
        return redirect('/auth/login/')
    elif len(usuario) > 0:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id
        return redirect('/plataforma/home/')


def sair(request):
    request.session.flush()
    return redirect('/auth/login/')