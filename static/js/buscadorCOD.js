// Este mini script permitira realizar una busqueda correcta por codigo y autor

// Buscamos por id en el form
// Parametros de busqueda "id = buscarCOD" "id = inputCOD"
// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("buscarCOD").addEventListener("submit", function(event) {
        event.preventDefault();

// Captura del campo
        var codigo = document.getElementById("inputCOD").value.trim();

        // Verificar que se haya ingresado un código
        if (codigo) {
            // Construir la URL /buscar/<codigo>
            var url = "/buscarcod/" + codigo;
            
            // Ir a URL construida
            window.location.href = url;
        } else {
            console.log("Debe ingresar algo valido");
        }
    });
});
