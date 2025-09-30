var contador = 1;
var celda = document.getElementsByClassName("celda");

for (let i = 0; i < celda.length; i++) {
    celda[i].addEventListener("click", function() {
        // Buscar los elementos dentro de esta celda específica
        var tache = this.querySelector(".tache");
        var circulo = this.querySelector(".circulo");
        
        // Verificar si la celda ya está ocupada
        if (tache.classList.contains("active") || circulo.classList.contains("active")) {
            return; // Salir si la celda ya tiene una ficha
        }
        
        if(contador % 2 !== 0){
            // Turno del tache
            tache.classList.remove("inactive");   
            tache.classList.add("active");
        } else {
            // Turno del círculo
            circulo.classList.remove("inactive");   
            circulo.classList.add("active");
        }
        contador += 1;
    });
}

