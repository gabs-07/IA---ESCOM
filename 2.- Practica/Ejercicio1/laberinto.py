import json
import random
import os
import copy
from collections import deque
#import heapq  # No se necesita porque A* está deshabilitado

# --------------------------
# Generar laberinto
# --------------------------

#creación del laberinto con backtracking
def crear_laberinto_con_backtracking(filas, columnas):
    laberinto_alto = filas * 2 + 1
    laberinto_ancho = columnas * 2 + 1
    laberinto = [['█'] * laberinto_ancho for _ in range(laberinto_alto)]

    # Poner las paredes exteriores
    def excavar(fila, col):
        laberinto[fila][col] = ' '
        direcciones = [(0,2),(0,-2),(2,0),(-2,0)]
        random.shuffle(direcciones)

        # Recorrer direcciones aleatorias
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            if 0 < nueva_fila < laberinto_alto and 0 < nueva_col < laberinto_ancho and laberinto[nueva_fila][nueva_col] == '█':
                laberinto[nueva_fila][nueva_col] = ' '
                laberinto[fila + df//2][col + dc//2] = ' '
                excavar(nueva_fila, nueva_col)

    excavar(1,1)
    return laberinto

# Añadir caminos adicionales al laberinto
def añadir_caminos(laberinto, numero_de_caminos=20):
    alto = len(laberinto)
    ancho = len(laberinto[0])
    # Arreglar caminos adicionales
    for _ in range(numero_de_caminos):
        fila = random.randint(1, alto-2)
        col = random.randint(1, ancho-2)
        if laberinto[fila][col] == '█':
            vecinos = sum([laberinto[fila+df][col+dc]==' ' for df,dc in [(-1,0),(1,0),(0,-1),(0,1)]])
            if vecinos >= 2:
                laberinto[fila][col] = ' '

# --------------------------
# Funciones para guardar laberinto
# --------------------------

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

# --------------------------
# Funciones BFS y DFS
# --------------------------
def reconstruir_camino(padres, inicio, meta):
    camino = []
    nodo = meta
    while nodo != inicio:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.append(inicio)
    camino.reverse()
    return camino

def bfs(laberinto, inicio, meta):
    filas, cols = len(laberinto), len(laberinto[0])
    visitados = set()
    padres = {}
    cola = deque([inicio])
    visitados.add(inicio)

    while cola:
        nodo = cola.popleft()
        if nodo == meta:
            return reconstruir_camino(padres, inicio, meta)
        x, y = nodo
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < filas and 0 <= ny < cols and laberinto[nx][ny] != '█' and (nx,ny) not in visitados:
                padres[(nx,ny)] = nodo
                visitados.add((nx,ny))
                cola.append((nx,ny))
    return None

def dfs(laberinto, inicio, meta):
    filas, cols = len(laberinto), len(laberinto[0])
    visitados = set()
    padres = {}
    pila = [inicio]
    visitados.add(inicio)

    while pila:
        nodo = pila.pop()
        if nodo == meta:
            return reconstruir_camino(padres, inicio, meta)
        x, y = nodo
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < filas and 0 <= ny < cols and laberinto[nx][ny] != '█' and (nx,ny) not in visitados:
                padres[(nx,ny)] = nodo
                visitados.add((nx,ny))
                pila.append((nx,ny))
    return None

# --------------------------
# Función mostrar laberinto
# --------------------------
def mostrar_laberinto(laberinto, camino, inicio, meta):
    lab = copy.deepcopy(laberinto)
    for (x,y) in camino:
        if (x,y) != inicio and (x,y) != meta:
            lab[x][y] = '*'
    lab[inicio[0]][inicio[1]] = 'S'
    lab[meta[0]][meta[1]] = 'E'
    for fila in lab:
        print(''.join(fila))
    print()

# --------------------------
# Función principal
# --------------------------
def main():
    filas_logicas, columnas_logicas = 20, 20
    laberinto = crear_laberinto_con_backtracking(filas_logicas, columnas_logicas)
    añadir_caminos(laberinto, 40)

    inicio = (1,1)
    meta = (len(laberinto)-2, len(laberinto[0])-2)

    print("Laberinto generado:")
    for fila in laberinto:
        print(''.join(fila))
    print()

    # BFS
    camino_bfs = bfs(laberinto, inicio, meta)
    print("Ruta BFS:")
    mostrar_laberinto(laberinto, camino_bfs, inicio, meta)

    # DFS
    camino_dfs = dfs(laberinto, inicio, meta)
    print("Ruta DFS:")
    mostrar_laberinto(laberinto, camino_dfs, inicio, meta)

    # Guardar el laberinto en archivos
    guardar_json(laberinto)
    guardar_apy(laberinto)

    # A* deshabilitado
    """
    # A*
    camino_a = a_estrella(laberinto, inicio, meta)
    print("Ruta A*:")
    mostrar_laberinto(laberinto, camino_a, inicio, meta)
    """

if __name__ == "__main__":
    main()
