// gato4x4.c
// Gato 4x4 con IA minimax + poda alfa-beta (consola).
// Humano = 'X', IA = 'O'.
// Compilar: gcc -O2 -std=c99 gato4x4.c -o gato4x4

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define EMPTY '.'
#define HUMAN 'X'
#define AI    'O'

#define INF 1000000000

// Líneas ganadoras (10)
static const int WIN_LINES[10][4] = {
    {0,1,2,3}, {4,5,6,7}, {8,9,10,11}, {12,13,14,15},
    {0,4,8,12}, {1,5,9,13}, {2,6,10,14}, {3,7,11,15},
    {0,5,10,15}, {3,6,9,12}
};

// Preferencia de casillas (centro primero) para acelerar la poda
static const int ORDER[16] = {5,6,9,10, 0,3,12,15, 1,2,4,7,8,11,13,14};

typedef struct {
    char cells[16];
} Board;

// PROTOTIPOS DE LAS FUNCIONES
void board_init(Board *b);
int is_full(const Board *b);
char winner(const Board *b);
void print_indices(void);
void print_board(const Board *b);
int terminal_value(const Board *b, int *is_terminal);
int count_empties(const Board *b);
int minimax(Board *b, int maximizing, int alpha, int beta);
int best_move(Board *b);
int read_move(void);

void board_init(Board *b) {
    int i;
    for (i = 0; i < 16; ++i) b->cells[i] = EMPTY;
}

int is_full(const Board *b) {
    int i;
    for (i = 0; i < 16; ++i) if (b->cells[i] == EMPTY) return 0;
    return 1;
}

char winner(const Board *b) {
    int i;
    for (i = 0; i < 10; ++i) {
        int a = WIN_LINES[i][0], c = WIN_LINES[i][1];
        int d = WIN_LINES[i][2], e = WIN_LINES[i][3];
        char x = b->cells[a];
        if (x != EMPTY &&
            b->cells[c] == x && b->cells[d] == x && b->cells[e] == x)
            return x;
    }
    return 0; // sin ganador
}

void print_indices(void) {
    puts("+----+----+----+----+");
    int r;
    for ( r = 0; r < 4; ++r) {
        printf("| %2d | %2d | %2d | %2d |\n", r*4, r*4+1, r*4+2, r*4+3);
        puts("+----+----+----+----+");
    }
}

void print_board(const Board *b) {
    puts("+---+---+---+---+");
    int r;
    for (r = 0; r < 4; ++r) {
        printf("| %c | %c | %c | %c |\n",
               b->cells[r*4], b->cells[r*4+1],
               b->cells[r*4+2], b->cells[r*4+3]);
        puts("+---+---+---+---+");
    }
}

// Función de utilidad para la IA (desde perspectiva de la IA)
int terminal_value(const Board *b, int *is_terminal) {
    char w = winner(b);
    if (w == AI) { *is_terminal = 1; return 100; }
    if (w == HUMAN) { *is_terminal = 1; return -100; }
    if (is_full(b)) { *is_terminal = 1; return 0; }
    *is_terminal = 0;
    return 0;
}

int count_empties(const Board *b) {
    int k = 0;
    int i;
    for (i = 0; i < 16; ++i) if (b->cells[i] == EMPTY) ++k; return k;
}

// Minimax con poda alfa-beta.
// maximizing = 1 si juega la IA; 0 si juega el humano.
int minimax(Board *b, int maximizing, int alpha, int beta) {
    int terminal, val = terminal_value(b, &terminal);
    if (terminal) {
        // Ajuste para preferir victorias rápidas y derrotas tardías
        int empties = count_empties(b);
        if (val > 0) return val + empties;   // ganar antes es mejor
        if (val < 0) return val - empties;   // perder después "menos peor"
        return 0;
    }

    if (maximizing) {
        int best = -INF;
        int k;
        for ( k = 0; k < 16; ++k) {
            int i = ORDER[k];
            if (b->cells[i] != EMPTY) continue;
            b->cells[i] = AI;
            int sc = minimax(b, 0, alpha, beta);
            b->cells[i] = EMPTY;
            if (sc > best) best = sc;
            if (best > alpha) alpha = best;
            if (beta <= alpha) break; // poda beta
        }
        return best;
    } else {
        int best = INF;
        int i;
        for ( i = 0; i < 16; ++i) {
            if (b->cells[i] != EMPTY) continue;
            b->cells[i] = HUMAN;
            int sc = minimax(b, 1, alpha, beta);
            b->cells[i] = EMPTY;
            if (sc < best) best = sc;
            if (best < beta) beta = best;
            if (beta <= alpha) break; // poda alfa
        }
        return best;
    }
}

int best_move(Board *b) {
    int alpha = -INF, beta = INF;
    int best_score = -INF, best_m = -1;

    int k;
    for ( k = 0; k < 16; ++k) {
        int i = ORDER[k];
        if (b->cells[i] != EMPTY) continue;
        b->cells[i] = AI;
        int sc = minimax(b, 0, alpha, beta);
        b->cells[i] = EMPTY;
        if (sc > best_score) {
            best_score = sc;
            best_m = i;
        }
        if (best_score > alpha) alpha = best_score;
    }
    return best_m;
}

int read_move(void) {
    char buf[64];
    if (!fgets(buf, sizeof(buf), stdin)) return -1;
    // permitir espacios/nueva línea
    int i = -1, ok = 0;
    int j;
    for ( j = 0; buf[j]; ++j) {
        if (isdigit((unsigned char)buf[j])) {
            if (i < 0) i = buf[j]-'0';
            else i = i*10 + (buf[j]-'0');
            ok = 1;
        } else if (ok) break;
    }
    return i;
}

int main(void) {
    Board board;
    board_init(&board);

    printf("Gato 4x4 — Humano (X) vs IA (O)\n");
    printf("Ingresa posiciones 0..15.\n\nÍndices:\n");
    print_indices();
    puts("");
    print_board(&board);

    int human_starts = 1;
    printf("¿Quieres empezar? (s/n) ");
    int ch = getchar();
    while (ch=='\n' || ch=='\r') ch = getchar();
    if (ch=='n' || ch=='N') human_starts = 0;
    // limpiar resto de línea
    int c; while ((c = getchar()) != '\n' && c != EOF) {}

    char turn = human_starts ? HUMAN : AI;

    while (1) {
        int term;
        int val = terminal_value(&board, &term);
        if (term) {
            print_board(&board);
            char w = winner(&board);
            if (w == HUMAN) puts("¡Ganaste! ??");
            else if (w == AI) puts("La IA ganó ??");
            else puts("Empate.");
            break;
        }

        if (turn == HUMAN) {
            int pos;
            printf("Tu jugada (0..15): ");
            pos = read_move();
            if (pos < 0 || pos > 15 || board.cells[pos] != EMPTY) {
                puts("Movimiento inválido, intenta de nuevo.");
                continue;
            }
            board.cells[pos] = HUMAN;
            turn = AI;
        } else {
            int m = best_move(&board);
            if (m >= 0) {
                board.cells[m] = AI;
                printf("La IA juega en %d\n", m);
            }
            turn = HUMAN;
        }
        print_board(&board);
    }

    return 0;
}
