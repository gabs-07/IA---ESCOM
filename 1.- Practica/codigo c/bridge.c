#include <stdio.h>
#include <stdlib.h>
#include <string.h>   // <- ESTA es la importante para strtok()

// Función auxiliar para imprimir un movimiento
void printMove(int a, int b) {
    if (b == -1) {
        printf("Persona %d cruza sola\n", a);
    } else {
        printf("Personas %d y %d cruzan\n", a, b);
    }
}

// Función recursiva para calcular el tiempo mínimo y mostrar movimientos
int minCrossingTime(int times[], int n) {
    if (n == 1) {
        printMove(times[0], -1);
        return times[0];
    }
    if (n == 2) {
        printMove(times[0], times[1]);
        return times[1];
    }
    if (n == 3) {
        printMove(times[0], times[1]);
        printMove(times[0], -1);
        printMove(times[0], times[2]);
        return times[0] + times[1] + times[2];
    }

    int option1 = times[1] + times[0] + times[n-1] + times[1];
    int option2 = times[n-1] + times[0] + times[n-2] + times[0];

    if (option1 < option2) {
        printMove(times[0], times[1]);
        printMove(times[0], -1);
        printMove(times[n-2], times[n-1]);
        printMove(times[1], -1);
        return option1 + minCrossingTime(times, n - 2);
    } else {
        printMove(times[0], times[n-1]);
        printMove(times[0], -1);
        printMove(times[0], times[n-2]);
        printMove(times[0], -1);
        return option2 + minCrossingTime(times, n - 2);
    }
}

int compare(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int bridgeAndTorch(int times[], int n) {
    qsort(times, n, sizeof(int), compare);
    return minCrossingTime(times, n);
}

int main() {
    char input[256];
    int times[100], n = 0;

    printf("Ingrese los tiempos separados por espacios:\n");
    fgets(input, sizeof(input), stdin);

    char *token = strtok(input, " ");
    while (token != NULL) {
        times[n++] = atoi(token);
        token = strtok(NULL, " ");
    }

    if (n == 0) {
        printf("No se ingresaron tiempos válidos.\n");
        return 1;
    }

    printf("\nSecuencia de cruces:\n");
    int total = bridgeAndTorch(times, n);

    printf("\nTiempo mínimo total = %d\n", total);
    return 0;
}
