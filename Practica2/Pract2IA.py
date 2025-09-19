## ----------------- LIBRERIAS ----------------- ##

import json     ## Para guardar la matriz en archivos JSON y APY
import random   ## Para generar números aleatorios
import os      ## Para operaciones del sistema (limpiar pantalla, manejar rutas)
import msvcrt ## Para capturar entradas de teclado en Windows

## ----------------- FUNCIONES ----------------- ##

## Funcion para limpiar la pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

## Funciones para crear el laberinto
def crear_laberinto_con_backtracking(filas, columnas):
    laberinto_alto = filas * 2 + 1
    laberinto_ancho = columnas * 2 + 1
    laberinto = [['█'] * laberinto_ancho for _ in range(laberinto_alto)]
    ## Poner las paredes exteriores
    def excavar(fila, col):
        laberinto[fila][col] = ' '
        
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones)

        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc

            if 0 < nueva_fila < laberinto_alto and 0 < nueva_col < laberinto_ancho and laberinto[nueva_fila][nueva_col] == '█':
                laberinto[nueva_fila][nueva_col] = ' '
                laberinto[fila + df // 2][col + dc // 2] = ' '
                excavar(nueva_fila, nueva_col)

    excavar(1, 1)

    return laberinto

## Función para añadir caminos adicionales al laberinto
def añadir_caminos(laberinto, numero_de_caminos=20):
    laberinto_alto = len(laberinto)
    laberinto_ancho = len(laberinto[0])

    for _ in range(numero_de_caminos):
        fila_aleatoria = random.randint(1, laberinto_alto - 2)
        col_aleatoria = random.randint(1, laberinto_ancho - 2)

        if laberinto[fila_aleatoria][col_aleatoria] == '█':
            vecinos_libres = 0
            if laberinto[fila_aleatoria - 1][col_aleatoria] == ' ': vecinos_libres += 1
            if laberinto[fila_aleatoria + 1][col_aleatoria] == ' ': vecinos_libres += 1
            if laberinto[fila_aleatoria][col_aleatoria - 1] == ' ': vecinos_libres += 1
            if laberinto[fila_aleatoria][col_aleatoria + 1] == ' ': vecinos_libres += 1

            if vecinos_libres >= 2:
                laberinto[fila_aleatoria][col_aleatoria] = ' '

## Funciones para guardar la matriz en archivos


# Obtiene la ruta del directorio donde se encuentra el script y guarda el archivo .json
ruta_del_directorio = os.path.dirname(os.path.abspath(__file__))

## Cambia el directorio de trabajo actual a la ruta del script
def guardar_json(laberinto, nombre_archivo="laberinto.json"):
    with open(nombre_archivo, 'w') as f:
        json.dump(laberinto, f, indent=4)
    print(f"Laberinto guardado en {nombre_archivo}")

## Cambia el directorio de trabajo actual a la ruta del script y guarda el archivo .apy
def guardar_apy(laberinto, nombre_archivo="laberinto.apy"):
    with open(nombre_archivo, 'w') as f:
        json.dump(laberinto, f, indent=4)
    print(f"Laberinto guardado en {nombre_archivo}")

## Función principal para jugar el laberinto
def jugar_laberinto():

    # Líneas para verificar el directorio de trabajo
    directorio_actual = os.getcwd()
    print(f"El laberinto se guardará en el siguiente directorio: {directorio_actual}\n")
    input("Presiona Enter para continuar...") # Pausa para que puedas ver el mensaje
    filas_logicas = 10
    columnas_logicas = 10

    # Crear el laberinto y añadir caminos
    laberinto = crear_laberinto_con_backtracking(filas_logicas, columnas_logicas)
    añadir_caminos(laberinto, numero_de_caminos=40)

    # Guardar el laberinto en archivos
    guardar_json(laberinto)
    guardar_apy(laberinto)

    # Posiciones iniciales del jugador y la meta
    jugador_fila, jugador_col = 1, 1 
    meta_fila, meta_col = len(laberinto) - 2, len(laberinto[0]) - 2
    
    # Colocar al jugador y la meta en el laberinto
    laberinto[jugador_fila][jugador_col] = 'S'
    laberinto[meta_fila][meta_col] = 'E'

    # Bucle principal del juego
    while True:
        clear_screen()
        print("Mueve al jugador (W, A, S, D). Salir: Q")
        for fila_mapa in laberinto:
            print(''.join(fila_mapa))

        # Verifica si el jugador ha llegado a la meta
        if jugador_fila == meta_fila and jugador_col == meta_col:
            print("\n¡Felicidades, llegaste a la meta!")
            break

        # Captura el movimiento del jugador
        movimiento = msvcrt.getch().decode().lower()

        # Calcula la nueva posición del jugador
        nueva_fila, nueva_col = jugador_fila, jugador_col

        # Mover según la entrada
        if movimiento == 'w': nueva_fila -= 1
        elif movimiento == 's': nueva_fila += 1
        elif movimiento == 'a': nueva_col -= 1
        elif movimiento == 'd': nueva_col += 1
        elif movimiento == 'q':
            print("Saliendo del juego.")
            break
        else:
            continue

        # Verifica si el movimiento es válido (dentro de los límites y no es una pared)
        if 0 <= nueva_fila < len(laberinto) and 0 <= nueva_col < len(laberinto[0]) and laberinto[nueva_fila][nueva_col] != '█':
            if laberinto[jugador_fila][jugador_col] != 'E':
                laberinto[jugador_fila][jugador_col] = '.'

            # Actualiza la posición del jugador
            jugador_fila, jugador_col = nueva_fila, nueva_col
            
            # Marca la nueva posición del jugador
            if laberinto[jugador_fila][jugador_col] != 'E':
                 laberinto[jugador_fila][jugador_col] = 'P'

# Llama a la función principal para iniciar el juego
jugar_laberinto()