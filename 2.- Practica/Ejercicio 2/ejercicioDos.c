#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 4
#define MAX_ESTADOS 100000

typedef struct {
    int tablero[N][N];
    int pasos;
    int padre;
    int heuristica;
} Estado;

// Prototipos de funciones
int iguales(int a[N][N], int b[N][N]);
void copiarTablero(int dest[N][N], int src[N][N]);
void buscarCero(int tablero[N][N], int *fila, int *col);
int manhattan(int tablero[N][N]);
void imprimirTablero(int tablero[N][N]);
int busquedaCiegas(int tableroInicial[N][N], Estado estados[MAX_ESTADOS], int *solucionIdx);
int busquedaA(int tableroInicial[N][N], Estado estados[MAX_ESTADOS], int *solucionIdx);
void imprimirSolucion(Estado estados[MAX_ESTADOS], int solucionIdx);

const int estadoMeta[N][N] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12},
    {13, 14, 15, 0}
};

const int movimientosPosibles[4][2] = {
    {-1,0}, {1,0}, {0,-1}, {0,1}
};

int iguales(int a[N][N], int b[N][N]) {
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++)
            if(a[i][j]!=b[i][j]) return 0;
    return 1;
}

void copiarTablero(int dest[N][N], int src[N][N]) {
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++)
            dest[i][j]=src[i][j];
}

void buscarCero(int tablero[N][N], int *fila, int *col) {
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++)
            if(tablero[i][j]==0) {
                *fila=i; *col=j; return;
            }
}

int manhattan(int tablero[N][N]) {
    int distanciaTotal=0;
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++) {
            int valor=tablero[i][j];
            if(valor!=0) {
                int filaMeta=(valor-1)/N;
                int colMeta=(valor-1)%N;
                distanciaTotal+=abs(i-filaMeta)+abs(j-colMeta);
            }
        }
    return distanciaTotal;
}

void imprimirTablero(int tablero[N][N]) {
    for(int i=0;i<N;i++) {
        for(int j=0;j<N;j++)
            printf("%2d ", tablero[i][j]);
        printf("\n");
    }
    printf("\n");
}

// BFS (búsqueda ciega)
int busquedaCiegas(int tableroInicial[N][N], Estado estados[MAX_ESTADOS], int *solucionIdx) {
    int visitados[MAX_ESTADOS]= {0};
    int frente=0, fondo=1;
    copiarTablero(estados[0].tablero, tableroInicial);
    estados[0].pasos=0; estados[0].padre=-1;
    while(frente<fondo) {
        Estado actual=estados[frente];
        if(iguales(actual.tablero, (int (*)[N])estadoMeta)) {
            *solucionIdx=frente;
            return 1;
        }
        int filaCero, colCero;
        buscarCero(actual.tablero, &filaCero, &colCero);
        for(int m=0;m<4;m++) {
            int nf=filaCero+movimientosPosibles[m][0];
            int nc=colCero+movimientosPosibles[m][1];
            if(nf>=0 && nf<N && nc>=0 && nc<N) {
                int nuevoTablero[N][N];
                copiarTablero(nuevoTablero, actual.tablero);
                nuevoTablero[filaCero][colCero]=nuevoTablero[nf][nc];
                nuevoTablero[nf][nc]=0;
                // Verificar si ya fue visitado
                int yaVisitado=0;
                for(int k=0;k<fondo;k++)
                    if(iguales(estados[k].tablero, nuevoTablero)) { yaVisitado=1; break; }
                if(!yaVisitado && fondo<MAX_ESTADOS) {
                    copiarTablero(estados[fondo].tablero, nuevoTablero);
                    estados[fondo].pasos=actual.pasos+1;
                    estados[fondo].padre=frente;
                    fondo++;
                }
            }
        }
        frente++;
    }
    return 0;
}

// A* (búsqueda informada)
int busquedaA(int tableroInicial[N][N], Estado estados[MAX_ESTADOS], int *solucionIdx) {
    int frente=0, fondo=1;
    copiarTablero(estados[0].tablero, tableroInicial);
    estados[0].pasos=0; estados[0].padre=-1;
    estados[0].heuristica=manhattan(tableroInicial);
    while(frente<fondo) {
        // Buscar el estado con menor heuristica+pasos
        int mejor=frente;
        for(int k=frente+1;k<fondo;k++)
            if(estados[k].pasos+estados[k].heuristica < estados[mejor].pasos+estados[mejor].heuristica)
                mejor=k;
        // Intercambiar
        Estado temp=estados[frente];
        estados[frente]=estados[mejor];
        estados[mejor]=temp;
        Estado actual=estados[frente];
        if(iguales(actual.tablero, (int (*)[N])estadoMeta)) {
            *solucionIdx=frente;
            return 1;
        }
        int filaCero, colCero;
        buscarCero(actual.tablero, &filaCero, &colCero);
        for(int m=0;m<4;m++) {
            int nf=filaCero+movimientosPosibles[m][0];
            int nc=colCero+movimientosPosibles[m][1];
            if(nf>=0 && nf<N && nc>=0 && nc<N) {
                int nuevoTablero[N][N];
                copiarTablero(nuevoTablero, actual.tablero);
                nuevoTablero[filaCero][colCero]=nuevoTablero[nf][nc];
                nuevoTablero[nf][nc]=0;
                // Verificar si ya fue visitado
                int yaVisitado=0;
                for(int k=0;k<fondo;k++)
                    if(iguales(estados[k].tablero, nuevoTablero)) { yaVisitado=1; break; }
                if(!yaVisitado && fondo<MAX_ESTADOS) {
                    copiarTablero(estados[fondo].tablero, nuevoTablero);
                    estados[fondo].pasos=actual.pasos+1;
                    estados[fondo].padre=frente;
                    estados[fondo].heuristica=manhattan(nuevoTablero);
                    fondo++;
                }
            }
        }
        frente++;
    }
    return 0;
}

void imprimirSolucion(Estado estados[MAX_ESTADOS], int solucionIdx) {
    int camino[MAX_ESTADOS], n=0;
    while(solucionIdx!=-1) {
        camino[n++]=solucionIdx;
        solucionIdx=estados[solucionIdx].padre;
    }
    for(int i=n-1;i>=0;i--)
        imprimirTablero(estados[camino[i]].tablero);
}

int main() {
    int tableroInicial[N][N]={
        {5, 1, 2, 4},
        {0, 6, 3, 8},
        {9, 10, 7, 12},
        {13, 14, 11, 15}
    };
    Estado estados[MAX_ESTADOS];
    int solucionIdx;
    printf("Solución búsqueda a ciegas (puede ser lenta):\n");
    if(busquedaCiegas(tableroInicial, estados, &solucionIdx))
        imprimirSolucion(estados, solucionIdx);
    else
        printf("No se encontró solución con búsqueda a ciegas.\n");

    printf("\nSolución búsqueda informada (A*):\n");
    if(busquedaA(tableroInicial, estados, &solucionIdx))
        imprimirSolucion(estados, solucionIdx);
    else
        printf("No se encontró solución con búsqueda informada.\n");
    return 0;
}


