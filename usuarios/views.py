from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse('Login')

def cadastro(request):
    return HttpResponse('cadastro')
# Create your views here.
