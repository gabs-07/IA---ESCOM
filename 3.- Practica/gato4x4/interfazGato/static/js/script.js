
var first = 'N';
var turno = 1; //turno%2 == 0 turno IA
var maxturno = turno;
var gato = [
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."]
];
const initGame = document.getElementById('start');

initGame.addEventListener("click", () => {
    turno = 0;
    enviarGato();
});

function reiniciar() {
    gato = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."]
    ];
    limpiarCeldas();
    turno = 1;
    limpiarButtonTurno();
}

function limpiarCeldas() {
    var celdas = Array.from(document.getElementsByClassName("celda"));
    celdas.forEach(celda => {
        celda.innerHTML = "";
    });
}

function limpiarButtonTurno() {
    const ia = document.getElementById('turnoIA');
    const jugador = document.getElementById('turnoJugador');

    ia.classList.add('gray');
    jugador.classList.add('gray');
}

function turnoIa() {
    const ia = document.getElementById('turnoIA');
    const jugador = document.getElementById('turnoJugador');

    jugador.classList.add('gray');
    ia.classList.remove('gray');
}

function turnoJug() {
    const ia = document.getElementById('turnoIA');
    const jugador = document.getElementById('turnoJugador');

    jugador.classList.remove('gray');
    ia.classList.add('gray');
}

function marcarCasilla(x, y, celda) {

    // turno<=15?cambiarButtonTurno():null;
    const i = x - 1;
    const j = y - 1;

    if (gato[i][j] != ".") {
        return showToast('error', 'Ya se ingresó un elemento');
    }

    if (maxturno >= 16) {
        return showToast('error', 'fin del juego');
    }

    gato[i][j] = turno % 2 == 0 ? "X" : "O";
    gato[i][j] == "O" ? turnoIa() : turnoJug();

    if (first == 'N') {
        first = gato[i][j];
    } else if (first == 'O') {
        first = 'T';
        maxturno--;
    } else {
        first == 'X';
    }

    agregarSimbolo(celda, gato[i][j]);
    if (gato[i][j] == "O") {
        enviarGato()
    }
    turno++;
    validarJuego();
}

function obtenerCelda(x, y) {
    const index = 4 * x + y;
    const celdas = document.getElementsByClassName("celda");
    return celdas[index];
}

function agregarSimbolo(celda, simbolo) {
    const simbolo_clase = simbolo === "X" ? "tache" : "circulo";
    const div = document.createElement("div");
    div.classList.add(simbolo_clase);
    celda.appendChild(div);
}

function enviarGato() {
    setTimeout(() => {
        const gatoDjango = gato;

        fetch("/obtener_jugada/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(gatoDjango)
        })
            .then(res => res.json())
            .then(data => {
                const x = data.x;
                const y = data.y;
                const t = data.t;
                const celda = obtenerCelda(x, y);
                marcarCasilla(x + 1, y + 1, celda);
            })
            .catch(err => console.error(err));
    }, 500); // 2000ms = 2 seconds
}

function showToast(type, message, duration = 2000) {
    const icons = {
        success: 'success',
        info: 'info',
        danger: 'error',
        error: 'error',
        warning: 'warning'
    };

    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: icons[type] || 'info',
        title: message,
        showConfirmButton: false,
        timer: duration,
        timerProgressBar: true
    });
}

var gato = [
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."]
];

const winningCombos = [
    // Rows
    [[0, 0], [0, 1], [0, 2], [0, 3]],
    [[1, 0], [1, 1], [1, 2], [1, 3]],
    [[2, 0], [2, 1], [2, 2], [2, 3]],
    [[3, 0], [3, 1], [3, 2], [3, 3]],

    // Columns
    [[0, 0], [1, 0], [2, 0], [3, 0]],
    [[0, 1], [1, 1], [2, 1], [3, 1]],
    [[0, 2], [1, 2], [2, 2], [3, 2]],
    [[0, 3], [1, 3], [2, 3], [3, 3]],

    // Diagonals
    [[0, 0], [1, 1], [2, 2], [3, 3]],
    [[0, 3], [1, 2], [2, 1], [3, 0]]
];

function verificarGanador(board) {
    for (const combo of winningCombos) {
        const [a, b, c, d] = combo;
        const v1 = board[a[0]][a[1]];
        const v2 = board[b[0]][b[1]];
        const v3 = board[c[0]][c[1]];
        const v4 = board[d[0]][d[1]];

        // Check if all four positions are the same and not empty (not ".")
        if (v1 !== "." && v1 === v2 && v1 === v3 && v1 === v4) {
            return v1; // Returns 'X' or 'O'
        }
    }
    return null; // No winner
}

// Usage example:
function validar() {
    const ganador = verificarGanador(gato);
    if (ganador !== null) {
        let mensaje = ganador === 'X' ? 'Ha ganado la IA' : 'Ha ganado el jugador';
        // showToast('success', mensaje);
        return true;
    }
    return false;
}

// Additional function to check for tie
function verificarEmpate(board) {
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (board[i][j] === ".") {
                return false; // There's still an empty space, game continues
            }
        }
    }
    return true; // All spaces are filled, it's a tie
}

// Complete validation function
function validarJuego() {
    const ganador = verificarGanador(gato);
    if (ganador) {
        let mensaje = ganador === 'X' ? 'Ha ganado la IA' : 'Ha ganado el jugador';
        console.log(mensaje);
        showToast('success', mensaje);
        turno = 10000;
        return { estado: 'ganador', jugador: ganador };
    }

    if (verificarEmpate(gato)) {
        showToast('error', `Empate`);
        return { estado: 'empate' };
    }

    return { estado: 'continuar' };
}

function showAlert(type, title, message) {
    const icons = {
        success: 'success',
        info: 'info',
        danger: 'error', // SweetAlert uses "error" instead of "danger"
        error: 'error'
    };

    Swal.fire({
        icon: icons[type] || 'info',
        title: title || '',
        text: message || '',
        confirmButtonText: 'OK'
    });
}