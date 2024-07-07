// Este mini script permitira realizar una busqueda correcta por codigo y autor

// Buscamos por id en el form
// Parametros de busqueda "id = buscarAUT" "id = inputAUT"
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("buscarAUT").addEventListener("submit", function (event) {
        event.preventDefault();

        // Captura del campo
        var autor = document.getElementById("inputAUT").value.trim();

        // Verificar que se haya ingresado un autor
        if (autor) {
            // Codificar el autor para incluirlo en la URL
            var autorCodificado = encodeURIComponent(autor);

            // Construir la URL /buscar/<autor>
            var url = "/buscaraut/" + autorCodificado;

            // Ir a URL construida
            window.location.href = url;
        } else {
            console.log("Debe ingresar algo valido");
        }
    });
});