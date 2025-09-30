import heapq
from collections import deque

# Estado objetivo del 15-puzzle
estadoMeta = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

# Movimientos posibles: (dx, dy)
# (-1,0): arriba, (1,0): abajo, (0,-1): izquierda, (0,1): derecha
movimientosPosibles = [(-1,0), (1,0), (0,-1), (0,1)]

def tableroATupla(tablero):
    """Convierte el tablero (lista de listas) a una tupla de tuplas para hashing."""
    return tuple(tuple(fila) for fila in tablero)

def buscarCero(tablero):
    """Encuentra la posición (fila, columna) del espacio vacío (0) en el tablero."""
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 0:
                return fila, columna
    return -1, -1

def vecinos(tablero):
    """Genera los tableros vecinos moviendo el espacio vacío en las direcciones posibles."""
    listaVecinos = []
    filaCero, columnaCero = buscarCero(tablero)
    for movFila, movColumna in movimientosPosibles:
        nuevaFila, nuevaColumna = filaCero + movFila, columnaCero + movColumna
        if 0 <= nuevaFila < 4 and 0 <= nuevaColumna < 4:
            nuevoTablero = [fila[:] for fila in tablero]
            nuevoTablero[filaCero][columnaCero], nuevoTablero[nuevaFila][nuevaColumna] = nuevoTablero[nuevaFila][nuevaColumna], nuevoTablero[filaCero][columnaCero]
            listaVecinos.append(nuevoTablero)
    return listaVecinos

def esMeta(tablero):
    """Verifica si el tablero es igual al estado meta."""
    return tablero == estadoMeta

def manhattan(tablero):
    """Calcula la suma de las distancias Manhattan de cada ficha a su posición objetivo."""
    distanciaTotal = 0
    for fila in range(4):
        for columna in range(4):
            valor = tablero[fila][columna]
            if valor != 0:
                filaMeta = (valor - 1) // 4
                columnaMeta = (valor - 1) % 4
                distanciaTotal += abs(fila - filaMeta) + abs(columna - columnaMeta)
    return distanciaTotal

def busquedaCiegas(tableroInicial):
    """Algoritmo de búsqueda a ciegas (BFS) para encontrar la solución."""
    cola = deque()
    cola.append((tableroInicial, []))
    estadosVisitados = set()
    estadosVisitados.add(tableroATupla(tableroInicial))
    while cola:
        tableroActual, camino = cola.popleft()
        if esMeta(tableroActual):
            return camino + [tableroActual]
        for vecinoTablero in vecinos(tableroActual):
            vecinoTupla = tableroATupla(vecinoTablero)
            if vecinoTupla not in estadosVisitados:
                estadosVisitados.add(vecinoTupla)
                cola.append((vecinoTablero, camino + [tableroActual]))
    return None

def busquedaA(tableroInicial):
    """Algoritmo de búsqueda informada (A*) usando la heurística de Manhattan."""
    monticulo = []
    heapq.heappush(monticulo, (manhattan(tableroInicial), 0, tableroInicial, []))
    estadosVisitados = set()
    estadosVisitados.add(tableroATupla(tableroInicial))
    while monticulo:
        costoEstimado, costoActual, tableroActual, camino = heapq.heappop(monticulo)
        if esMeta(tableroActual):
            return camino + [tableroActual]
        for vecinoTablero in vecinos(tableroActual):
            vecinoTupla = tableroATupla(vecinoTablero)
            if vecinoTupla not in estadosVisitados:
                estadosVisitados.add(vecinoTupla)
                nuevoCosto = costoActual + 1
                heuristica = manhattan(vecinoTablero)
                heapq.heappush(monticulo, (nuevoCosto + heuristica, nuevoCosto, vecinoTablero, camino + [tableroActual]))
    return None

def imprimirTablero(tablero):
    """Imprime el tablero de forma legible."""
    for fila in tablero:
        print(' '.join(str(x).rjust(2) for x in fila))
    print()

if __name__ == "__main__":
    # Estado inicial (puedes modificarlo)
    tableroInicial = [
        [5, 1, 2, 4],
        [0, 6, 3, 8],
        [9, 10, 7, 12],
        [13, 14, 11, 15]
    ]
    print("Solución búsqueda a ciegas (puede ser lenta):")
    solucionCiegas = busquedaCiegas(tableroInicial)
    if solucionCiegas:
        for tablero in solucionCiegas:
            imprimirTablero(tablero)
    else:
        print("No se encontró solución con búsqueda a ciegas.")

    print("\nSolución búsqueda informada (A*):")
    solucionA = busquedaA(tableroInicial)
    if solucionA:
        for tablero in solucionA:
            imprimirTablero(tablero)
    else:
        print("No se encontró solución con búsqueda informada.")


