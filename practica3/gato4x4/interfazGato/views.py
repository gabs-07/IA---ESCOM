from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

def gato(request):
    template = loader.get_template('interfaz.html')
    return HttpResponse(template.render())