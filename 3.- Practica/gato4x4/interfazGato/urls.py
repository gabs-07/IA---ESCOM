from django.urls import path
from . import views

urlpatterns = [
    path('', views.gato, name='gato'),
    path('obtener_jugada/', views.datosJS, name='obtener_jugada')
]
