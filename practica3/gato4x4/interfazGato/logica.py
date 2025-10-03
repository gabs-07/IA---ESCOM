# --- Configuración del Tablero ---
import math
import random

PROFUNDIDAD_MAXIMA = 6 # Prueba con 6; si es lento, baja a 4. Si es rápido, sube a 8.
TAMANO = 4
FICHA_VACIA = '.'

tablero = [[FICHA_VACIA for _ in range(TAMANO)] for _ in range(TAMANO)]
# ---------------------------------

def imprimir_tablero_estilizado(tablero):
    """Imprime el tablero de 4x4 con líneas divisorias verticales y horizontales."""
    print("\n  1 | 2 | 3 | 4 ")
    horizontal_line = "----+---+---+---"
    
    for i in range(TAMANO):
        # La línea de contenido de la fila
        row_content = f"{i+1} {tablero[i][0]} | {tablero[i][1]} | {tablero[i][2]} | {tablero[i][3]} "
        print(row_content)
        
        # Imprime la línea horizontal después de cada fila, excepto la última
        if i < TAMANO - 1:
            print(horizontal_line)
    print()

def evaluar_heuristica(tablero, jugador):
    """
    Función heurística: puntúa el tablero contando líneas de 2, 3 o 4.
    Un mayor puntaje significa que el jugador está más cerca de ganar.
    """
    puntuacion = 0
    oponente = 'O' if jugador == 'X' else 'X'

    for i in range(TAMANO):
        for j in range(TAMANO):
            if tablero[i][j] == jugador:
                # Simplificación: Puntuamos líneas de 3 (más valiosas) y 4 (victoria)
                # La victoria se maneja en la condición base, pero aquí sumamos si está muy cerca.
                
                # Ejemplo de chequeo de 3 en raya (horizontal)
                if j <= TAMANO - 3 and all(tablero[i][k] == jugador for k in range(j, j + 3)):
                    # Contamos 3 seguidas que pueden ser 4
                    if j > 0 and tablero[i][j-1] == FICHA_VACIA or j < TAMANO - 3 and tablero[i][j+3] == FICHA_VACIA:
                         puntuacion += 10 # Cerca de ganar
                         
    # Penalizar al oponente
    # NOTA: En la práctica, se puntúa de forma más sofisticada, contando amenazas abiertas.
    
    return puntuacion
    
def evaluar_tablero(tablero):
    """Evalúa los estados finales O usa la heurística."""
    
    # Estados finales tienen prioridad
    if verificar_ganador(tablero, 'X'): return 10000000 # Puntaje muy alto para asegurar la victoria
    if verificar_ganador(tablero, 'O'): return -10000000 # Puntaje muy bajo para asegurar la derrota
    
    # Usar heurística si no es un estado final
    score_x = evaluar_heuristica(tablero, 'X')
    score_o = evaluar_heuristica(tablero, 'O')
    
    return score_x - score_o # Retornamos la diferencia (Maximizar el puntaje de X y minimizar el de O)

def obtener_jugada(jugador, tablero):
    """Pide al usuario que ingrese una jugada y valida la entrada."""
    while True:
        try:
            print(f"Turno del jugador '{jugador}'.")
            fila = int(input("Ingresa el número de fila (1-4): "))
            columna = int(input("Ingresa el número de columna (1-4): "))

            idx_fila = fila - 1
            idx_columna = columna - 1

            # 1. Validar que los números estén dentro del rango 1 a 4
            if not (1 <= fila <= TAMANO and 1 <= columna <= TAMANO):
                print(f"❌ ERROR: Los números de fila y columna deben estar entre 1 y {TAMANO}.")
                continue

            # 2. Validar que la casilla esté vacía ('.')
            if tablero[idx_fila][idx_columna] != FICHA_VACIA:
                print("❌ ERROR: La casilla ya está ocupada. Elige otra.")
                continue
            
            return idx_fila, idx_columna

        except ValueError:
            print("❌ ERROR: Entrada no válida. Por favor, ingresa un número.")

def verificar_ganador(tablero, jugador):
    """Verifica si el jugador actual ha ganado (4 en raya)."""
    # 1. Horizontales y Verticales
    for i in range(TAMANO):
        if all(tablero[i][j] == jugador for j in range(TAMANO)): return True
        if all(tablero[j][i] == jugador for j in range(TAMANO)): return True
    # 2. Diagonal Principal (\)
    if all(tablero[i][i] == jugador for i in range(TAMANO)): return True
    # 3. Diagonal Secundaria (/)
    if all(tablero[i][TAMANO - 1 - i] == jugador for i in range(TAMANO)): return True
    return False

def tablero_lleno(tablero):
    """Verifica si no quedan más movimientos."""
    return all(FICHA_VACIA not in fila for fila in tablero)

def get_movimientos_validos(tablero):
    """Devuelve una lista de tuplas (fila, columna) de movimientos disponibles."""
    movimientos = []
    for r in range(TAMANO):
        for c in range(TAMANO):
            if tablero[r][c] == FICHA_VACIA:
                movimientos.append((r, c))
    return movimientos

# --- Algoritmo Minimax con Poda Alfa-Beta ---

def evaluar_tablero(tablero):
    """Asigna un puntaje al estado actual del tablero."""
    if verificar_ganador(tablero, 'X'):
        return 100  # IA gana (MAX)
    if verificar_ganador(tablero, 'O'):
        return -100 # Jugador pierde (MIN)
    return 0 # Empate o juego inconcluso

def minimax_ab(tablero, profundidad, alfa, beta, es_maximizador):
    """
    Función recursiva de Minimax con Poda Alfa-Beta.
    
    :param es_maximizador: True si es el turno de la IA ('X'), False si es el turno del oponente ('O').
    """
    if profundidad == PROFUNDIDAD_MAXIMA or tablero_lleno(tablero) or verificar_ganador(tablero, 'X') or verificar_ganador(tablero, 'O'):
        return evaluar_tablero(tablero)
    
    # Condición base: El juego terminó o se alcanzó la profundidad máxima
    puntuacion = evaluar_tablero(tablero)
    if puntuacion != 0 or tablero_lleno(tablero):
        return puntuacion
    
    movimientos_validos = get_movimientos_validos(tablero)

    if es_maximizador: # Turno de la IA (MAX)
        max_eval = -math.inf
        
        for r, c in movimientos_validos:
            # 1. Hacer el movimiento
            tablero[r][c] = 'X'
            
            # 2. Llamada recursiva
            evaluacion = minimax_ab(tablero, profundidad + 1, alfa, beta, False)
            
            # 3. Deshacer el movimiento (backtracking)
            tablero[r][c] = FICHA_VACIA
            
            # 4. Actualizar MAX y Alfa
            max_eval = max(max_eval, evaluacion)
            alfa = max(alfa, evaluacion)
            
            # 5. PODA BETA: Si Alfa es mayor o igual a Beta, se poda el resto de la rama
            if beta <= alfa:
                break 
                
        return max_eval

    else: # Turno del Oponente (MIN)
        min_eval = math.inf
        
        for r, c in movimientos_validos:
            # 1. Hacer el movimiento
            tablero[r][c] = 'O'
            
            # 2. Llamada recursiva
            evaluacion = minimax_ab(tablero, profundidad + 1, alfa, beta, True)
            
            # 3. Deshacer el movimiento (backtracking)
            tablero[r][c] = FICHA_VACIA
            
            # 4. Actualizar MIN y Beta
            min_eval = min(min_eval, evaluacion)
            beta = min(beta, evaluacion)
            
            # 5. PODA ALFA: Si Alfa es mayor o igual a Beta, se poda el resto de la rama
            if beta <= alfa:
                break
                
        return min_eval

def encontrar_mejor_jugada(tablero):
    """Itera sobre todos los movimientos y usa Minimax para encontrar el mejor."""
    mejor_eval = -math.inf
    mejor_movimiento = None
    
    for r, c in get_movimientos_validos(tablero):
        # 1. Hacer el movimiento (temporalmente)
        tablero[r][c] = 'X'
        
        # 2. Evaluar el tablero con Minimax (el siguiente turno será MIN)
        # Inicializar alfa y beta
        evaluacion = minimax_ab(tablero, 0, -math.inf, math.inf, False)
        
        # 3. Deshacer el movimiento
        tablero[r][c] = FICHA_VACIA
        
        # 4. Actualizar la mejor jugada
        if evaluacion > mejor_eval:
            mejor_eval = evaluacion
            mejor_movimiento = (r, c)
            
    return mejor_movimiento

# ... (mantener todas las funciones anteriores: imprimir_tablero_estilizado, obtener_jugada, etc.)

def jugar_4x4_tictactoe_con_ia():
    global tablero # Asegúrate de que estás usando el tablero global
    tablero = [[FICHA_VACIA for _ in range(TAMANO)] for _ in range(TAMANO)] # Reiniciar tablero
    
    jugadas = 0
    
    # La IA será 'X' y el jugador humano será 'O'
    jugadores = {'X': 'IA', 'O': 'Humano'} 

    print("--- ⚔️  Tic-Tac-Toe 4x4 vs IA (X) ⚔️ ---")
    imprimir_tablero_estilizado(tablero)

    while True:
        jugador_actual = 'X' if jugadas % 2 == 0 else 'O'
        
        if jugador_actual == 'X':
            # Turno de la IA
            print("Turno de la IA ('X'). Calculando mejor jugada...")
            r, c = encontrar_mejor_jugada(tablero)
            print(f"La IA juega en Fila {r+1}, Columna {c+1}")
            
        else:
            # Turno del Humano ('O')
            r, c = obtener_jugada(jugador_actual, tablero)
        
        # 1. Aplicar Jugada
        tablero[r][c] = jugador_actual
        jugadas += 1
        
        # 2. Imprimir el tablero actualizado
        imprimir_tablero_estilizado(tablero)

        # 3. Verificar Ganador
        if verificar_ganador(tablero, jugador_actual):
            ganador = jugadores[jugador_actual]
            print(f"🎉 ¡El {ganador} ('{jugador_actual}') ha ganado la partida! 🎉")
            break

        # 4. Verificar Empate
        if tablero_lleno(tablero):
            print("➖ El tablero está lleno. ¡Es un empate! ➖")
            break
