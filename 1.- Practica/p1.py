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

#Librerias: 
# Librerias: 
import tkinter as tk
from itertools import combinations

# Variables globales
persona = [1, 2, 5, 10]
text_result = None  # lo usamos para mostrar resultados en Tkinter

def imprimirTitulo(): 
    return "\n Practica Uno: The bridge and torch problem \n"

def timeOptimo(persona):
    # Estado inicial
    inicial = (frozenset(persona), frozenset(), 0, 'izq')  
    soluciones = []
    mejorTiempo = [float('inf')]

    def dfs(izq, der, tiempo, antorcha, camino):
        if tiempo >= mejorTiempo[0]:
            return

        if not izq:
            if tiempo < mejorTiempo[0]:
                mejorTiempo[0] = tiempo
                soluciones.clear()
                soluciones.append((tiempo, camino[:]))
            elif tiempo == mejorTiempo[0]:
                soluciones.append((tiempo, camino[:]))
            return

        if antorcha == 'izq':
            for a, b in combinations(izq, 2):
                nuevoTiempo = tiempo + max(a, b)
                nuevoIzq = set(izq) - {a, b}
                nuevoDer = set(der) | {a, b}
                dfs(frozenset(nuevoIzq), frozenset(nuevoDer), nuevoTiempo, 'der',
                    camino + [f"{a},{b} → ({max(a,b)})"])
        else:
            for a in der:
                nuevoTiempo = tiempo + a
                nuevoIzq = set(izq) | {a}
                nuevoDer = set(der) - {a}
                dfs(frozenset(nuevoIzq), frozenset(nuevoDer), nuevoTiempo, 'izq',
                    camino + [f"{a} ← ({a})"])

    # Llamada inicial
    dfs(inicial[0], inicial[1], inicial[2], inicial[3], [])
    return soluciones

def imprimirResultados():
    soluciones = timeOptimo(persona)
    # limpiar antes de escribir
    text_result.delete("1.0", tk.END)  
    text_result.insert(tk.END, imprimirTitulo())
    text_result.insert(tk.END, f"Mejor tiempo: {soluciones[0][0]} minutos\n\n")
    text_result.insert(tk.END, "Una de las soluciones óptimas:\n")
    for pasoDado in soluciones[0][1]:
        text_result.insert(tk.END, f"  {pasoDado}\n")

def main():
    global text_result
    ventana = tk.Tk()
    ventana.title("The Bridge and Torch Problem")
    ventana.geometry("500x400")

    label_title = tk.Label(ventana, text="Practica Uno: The Bridge and Torch Problem", font=("Arial", 14, "bold"))
    label_title.pack(pady=10)

    btn_run = tk.Button(ventana, text="Resolver", command=imprimirResultados, 
                        font=("Arial", 12), bg="#FF0000", fg="white")
    btn_run.pack(pady=10)

    text_result = tk.Text(ventana, wrap="word", font=("Consolas", 11))
    text_result.pack(expand=True, fill="both", padx=10, pady=10)

    ventana.mainloop()

main()
