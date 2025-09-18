import json
import heapq

# Puntos de inicio y fin del laberinto
START_POS = (1, 1)
END_POS = (19, 19)
MAZE_FILENAME = 'laberinto.json'

class Node:
    """Clase para representar un nodo en el laberinto."""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Costo desde el inicio
        self.h = 0  # Costo heurístico al final
        self.f = 0  # Costo total (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def heuristic(current_pos, end_pos):
    """Calcula la distancia de Manhattan entre dos puntos."""
    return abs(current_pos[0] - end_pos[0]) + abs(current_pos[1] - end_pos[1])

def load_maze(filename):
    """Carga el laberinto desde un archivo JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            maze_data = json.load(f)
        return maze_data
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{filename}' tiene un formato JSON inválido.")
        return None

def solve_a_star(maze, start, end):
    """Resuelve el laberinto usando el algoritmo A*."""
    start_node = Node(None, start)
    end_node = Node(None, end)
    
    # open_list es una cola de prioridad (min-heap)
    open_list = [(start_node.f, start_node)]
    closed_list = set()
    
    while open_list:
        current_f, current_node = heapq.heappop(open_list)
        
        if current_node.position in closed_list:
            continue
        
        closed_list.add(current_node.position)

        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Retorna el camino invertido

        # Generar los nodos hijos (vecinos)
        neighbors = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Arriba, Abajo, Izquierda, Derecha
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Verificar si la posición es válida (dentro de los límites y no es un muro)
            if (0 <= node_position[0] < len(maze) and
                0 <= node_position[1] < len(maze[0]) and
                maze[node_position[0]][node_position[1]] != "\u2588"):

                if node_position not in closed_list:
                    new_node = Node(current_node, node_position)
                    neighbors.append(new_node)
        
        for neighbor in neighbors:
            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor.position, end_node.position)
            neighbor.f = neighbor.g + neighbor.h
            
            found_in_open = False
            for f_val, node_in_open in open_list:
                if neighbor == node_in_open and f_val <= neighbor.f:
                    found_in_open = True
                    break
            
            if not found_in_open:
                heapq.heappush(open_list, (neighbor.f, neighbor))

    return None

def print_solution(maze, path, start_pos, end_pos):
    """Imprime el laberinto con el camino resuelto."""
    solution_maze = [list(row) for row in maze]
    
    if path:
        for (r, c) in path:
            if solution_maze[r][c] == ' ':
                solution_maze[r][c] = "*"
        solution_maze[start_pos[0]][start_pos[1]] = "S"
        solution_maze[end_pos[0]][end_pos[1]] = "E"
        
    for row in solution_maze:
        print("".join(row))

if __name__ == "__main__":
    maze_data = load_maze(MAZE_FILENAME)
    
    if maze_data:
        solution_path = solve_a_star(maze_data, START_POS, END_POS)
        
        if solution_path:
            print("¡Laberinto resuelto con el algoritmo A*! 🎉")
            print_solution(maze_data, solution_path, START_POS, END_POS)
        else:
            print("No se encontró una solución.")