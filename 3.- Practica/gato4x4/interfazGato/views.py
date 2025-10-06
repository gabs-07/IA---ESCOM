from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import logica

def gato(request):
    template = loader.get_template('interfaz.html')
    return HttpResponse(template.render())

@csrf_exempt
def datosJS(request):
    if request.method == "POST":
        gato = json.loads(request.body)
        print("Matriz recibida:", gato)
        x, y = logica.encontrar_mejor_jugada(gato)
        t = logica.verificar_ganador(gato, 'X')
        print("valor t: ", t)

        print(x,y)
        return JsonResponse({"x":x, "y":y,"t":t})

    return JsonResponse({"error": "Método no permitido"}, status=405)


