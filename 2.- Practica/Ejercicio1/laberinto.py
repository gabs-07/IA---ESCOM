import json
import random
import os
import copy
from collections import deque
import heapq

# --------------------------
# Generar laberinto
# --------------------------

def crear_laberinto_con_backtracking(filas, columnas):
    laberinto_alto = filas * 2 + 1
    laberinto_ancho = columnas * 2 + 1
    laberinto = [['█'] * laberinto_ancho for _ in range(laberinto_alto)]

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

def añadir_caminos(laberinto, numero_de_caminos=20):
    alto = len(laberinto)
    ancho = len(laberinto[0])
    for _ in range(numero_de_caminos):
        fila = random.randint(1, alto - 2)
        col = random.randint(1, ancho - 2)
        if laberinto[fila][col] == '█':
            vecinos = sum([laberinto[fila + df][col + dc] == ' ' for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]])
            if vecinos >= 2:
                laberinto[fila][col] = ' '

# --------------------------
# Funciones para guardar laberinto
# --------------------------

# Directorio del script
ruta_del_directorio = os.path.dirname(os.path.abspath(__file__))

def guardar_json(laberinto, nombre_archivo="laberinto.json"):
    ruta_completa = os.path.join(ruta_del_directorio, nombre_archivo)
    with open(ruta_completa, 'w') as f:
        json.dump(laberinto, f, indent=4)
    print(f"Laberinto guardado en {ruta_completa}")

def guardar_apy(laberinto, nombre_archivo="laberinto.apy"):
    ruta_completa = os.path.join(ruta_del_directorio, nombre_archivo)
    with open(ruta_completa, 'w') as f:
        json.dump(laberinto, f, indent=4)
    print(f"Laberinto guardado en {ruta_completa}")

# --------------------------
# BFS, DFS y A*
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
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < cols and laberinto[nx][ny] != '█' and (nx, ny) not in visitados:
                padres[(nx, ny)] = nodo
                visitados.add((nx, ny))
                cola.append((nx, ny))
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
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < cols and laberinto[nx][ny] != '█' and (nx, ny) not in visitados:
                padres[(nx, ny)] = nodo
                visitados.add((nx, ny))
                pila.append((nx, ny))
    return None

def a_estrella(laberinto, inicio, meta):
    filas, cols = len(laberinto), len(laberinto[0])
    g_cost = {inicio: 0}
    f_cost = {inicio: h(inicio, meta)}
    cola_prioridad = [(f_cost[inicio], inicio)]
    padres = {inicio: None}

    while cola_prioridad:
        f, nodo = heapq.heappop(cola_prioridad)

        if nodo == meta:
            return reconstruir_camino(padres, inicio, meta)

        x, y = nodo
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)

            if 0 <= nx < filas and 0 <= ny < cols and laberinto[nx][ny] != '█':
                nuevo_g_cost = g_cost[nodo] + 1
                if vecino not in g_cost or nuevo_g_cost < g_cost[vecino]:
                    g_cost[vecino] = nuevo_g_cost
                    f_cost[vecino] = nuevo_g_cost + h(vecino, meta)
                    padres[vecino] = nodo
                    heapq.heappush(cola_prioridad, (f_cost[vecino], vecino))
    return None

def h(nodo, meta):
    return abs(nodo[0] - meta[0]) + abs(nodo[1] - meta[1])

# --------------------------
# Mostrar laberinto
# --------------------------

def mostrar_laberinto(laberinto, camino, inicio, meta):
    lab = copy.deepcopy(laberinto)
    if camino:
        for (x, y) in camino:
            if (x, y) != inicio and (x, y) != meta:
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
    filas_logicas, columnas_logicas = 10, 10
    laberinto = crear_laberinto_con_backtracking(filas_logicas, columnas_logicas)
    añadir_caminos(laberinto, 40)

    inicio = (1, 1)
    meta = (len(laberinto) - 2, len(laberinto[0]) - 2)

    print("Laberinto generado:")
    for fila in laberinto:
        print(''.join(fila))
    print()

    # BFS
    print("Ruta BFS:")
    camino_bfs = bfs(laberinto, inicio, meta)
    mostrar_laberinto(laberinto, camino_bfs, inicio, meta)

    # DFS
    print("Ruta DFS:")
    camino_dfs = dfs(laberinto, inicio, meta)
    mostrar_laberinto(laberinto, camino_dfs, inicio, meta)

    # A*
    print("Ruta A*:")
    camino_a_estrella = a_estrella(laberinto, inicio, meta)
    mostrar_laberinto(laberinto, camino_a_estrella, inicio, meta)

    # Guardar laberinto
    guardar_json(laberinto)
    guardar_apy(laberinto)

if __name__ == "__main__":
    main()