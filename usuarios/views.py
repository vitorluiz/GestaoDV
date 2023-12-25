from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256

def login(request):
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

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')
    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')
    
    usuario = Usuario.objects.filter(email=email)

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')
    
    try:

        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome=nome,
                        senha=senha,
                        email=email,
                        telefone=telefone)
        usuario.save()
        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')
    
def valida_login(request):

    senha = request.POST.get('senha')
    email = request.POST.get('email')

    senha = sha256(senha.encode()).hexdigest()
   
    usuario = Usuario.objects.filter(email=email).filter(senha=senha)

    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['logado'] = True
        return redirect('/plataforma/home/')

def sair(request):
    request.session['logado'] = None
    return redirect('/auth/login/')