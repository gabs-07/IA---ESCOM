# Elabora un programa que resuelva este rompecabezas:
# "The bridge and torch problem"
# El enunciado del problema es el siguiente:

# Cuatro individuos llegan a un río de noche. Hay un puente estrecho, pero este solo soporta a dos personas a la vez. Los individuos 
# tienen una antorcha y, debido a que es de noche, deben utilizarla cuando cruzan el puente; por lo tanto, si cruzan dos personas, 
# uno debe volver atrás llevando la antorcha para que puedan cruzar los demás. El individuo A puede cruzar el puente en un minuto, 
# el individuo B en dos minutos, el individuo C en cinco minutos, y el individuo D en ocho minutos. Cuando dos individuos cruzan el 
# puente juntos, tardan lo que tarda el más lento de ellos.

# Tu programa deberá recibir una lista que represente el tiempo que tarda cada sujeto en cruzar el puente.
# La salida consiste en generar todos los movimientos de los sujetos, de forma que todos crucen el puente en el menor tiempo posible.

# [1,2,5,10] el óptimo es 17:
# (1,2) → 2; 1 ← 1; (5,10) → 10; 2 ← 2; (1,2) → 2. Total = 17.


# Prototipo de la funcion: 

def imprimirTitulo(): 
    print("\n Practica Uno: The bridge and torch problem \n")

def main():
    imprimirTitulo()

#Definicionde las funciones:
main()
