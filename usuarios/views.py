from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'login.html')

def cadastro(request):

    return render(request, 'cadastro.html') 

def valida_cadastro(request):
    nome = request.POST.get('nome')
    telefone = request.POST.get('telefone')
    email = request.POST.get('email')
    return HttpResponse(f'{nome}-{telefone}-{email}')