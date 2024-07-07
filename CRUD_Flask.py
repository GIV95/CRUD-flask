"""
Esta cabezera contiene todo lo necesario para realizar solicitudes.
La API se vincula con la clase "BiblioteClassSQL.py", queda modular.

Se importa la biblioteca "logging" para poder ver todos los -print- por consola
vale aclarar que no se definieron alertas del tipo "logging".
"""

from SQL.BibliotecaClassSQL import *
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_cors import CORS
import logging # Para ver todas las alertas por consola

# Configuración de logging para mostrar todos los registros en la consola
logging.basicConfig(level=logging.DEBUG)

# Datos de conexion por defecto
# Para -debug- colocar los que se utiliza en cada PC

db_host = "localhost"
db_user = "root"
db_pass = "0000"

#-----------------------------------------------------------------------------------------------------------------------------
# Comienza la API
app = Flask(__name__)
CORS(app) # Con esto logramos entrar desde cualquier punto 

# Instanciado de la base de datos y conexion
bibliotecaDB = Biblioteca(host = db_host,
                          user = db_user,
                          password = db_pass
                          )

#-----------------------------------------------------------------------------------------------------------------------------
# Presenta todos los libros en la base de datos
# Por Jinja2 permitira ver los datos en la web
@app.route('/listar_libros')
def listar_libros():
    libros = bibliotecaDB.mostrarTODOS_libro()
    if libros:
        return render_template('listar_libros.html', libros=libros)
    else:
        return jsonify({'Advertencia':'No se encuentran los libros'})
 
#-----------------------------------------------------------------------------------------------------------------------------
# Agregar libro
# Entrada al formulario para nuevo libro.
@app.route('/nuevo_libro', methods=['GET'])
def nuevo_formulario():
    return render_template('nuevo_libro.html')

# Recepcion del formulario de nuevo libro. 
@app.route('/nuevo_libro', methods = ['POST'])
def nuevo_libro():
    autor = request.form.get('autor')
    titulo = request.form.get('titulo')
    portada = request.form.get('portada')

    if not autor or not titulo:
        return jsonify({"mensaje": "Faltan datos"})

    libro_id = bibliotecaDB.agregar_Libro(autor, titulo, portada)

    if libro_id:
        return redirect(url_for('listar_libros'))
    else:
        return jsonify({"mensaje": "No se pudo agregar nuevo libro"})

#-----------------------------------------------------------------------------------------------------------------------------
# Eliminar libro. Eliminar por autor no esta implementada en la web
@app.route('/eliminar_codigo/<int:codigo>',methods = ['DELETE'])
def eliminar_codigo(codigo):
    eliminado = bibliotecaDB.eliminarCODIGO_Libro(codigo)
    if eliminado:
        return redirect(url_for('listar_libros'))
    else:
        return jsonify({'Advertencia':'No se puede eliminar libro por codigo'})

@app.route('/eliminar_autor/<string:autor>',methods = ['DELETE'])
def eliminar_autor(autor):
    eliminado = bibliotecaDB.eliminarAUTOR_Libro(autor)
    if eliminado:
        return jsonify({"mensaje": f"Libros del {autor} eliminados."})
    else:
        return jsonify({'Advertencia':'No se puede eliminar libro/s por autor'})

#-----------------------------------------------------------------------------------------------------------------------------
# Modificar libro 
# Se parciona en dos partes, primero recibe solicitud GET y luego un POST al completar el formulario
# 1) Entrada a la ruta con formulario, por codigo. Se extrean los datos de ese codigo.
@app.route('/modificar_libro/<int:codigo>', methods = ['GET'])
def modificar_formulario(codigo):
    libro = bibliotecaDB.buscarCODIGO_Libro(codigo)
    if libro:
        return render_template('modificar_libro.html', libro=libro)
    else:
        return jsonify({"mensaje": f"No se encontró libro con código {codigo}"})

# 2) Recepcion del formulario y edicion. Desde el formulario se activa el metodo PUT y se modifica el libro. 
# ESTO TENDRIA QUE SER UN PUT y una sola entrada - FUNCIONAR FUNCIONA PERO NO ES BUENA PRACTICA
@app.route('/modificar_libro/<int:codigo>', methods=['PUT','POST'])
def modificar_libro(codigo):
    autor = request.form.get('autor')
    titulo = request.form.get('titulo')
    portada = request.form.get('portada')

    if not autor or not titulo:
        return jsonify({"mensaje": "Faltan datos"})

    modificado = bibliotecaDB.modificar_Libro(codigo, autor, titulo, portada)

    if modificado:
        return redirect(url_for('listar_libros'))  # Redirige a la lista de libros después de modificar
    else:
        return jsonify({"mensaje": f"No se pudo modificar libro con código {codigo}"})

#-----------------------------------------------------------------------------------------------------------------------------
# Buscador de libros
@app.route('/buscarcod/<int:codigo>', methods = ['GET'])
def buscar_codigo(codigo):
    libro = bibliotecaDB.buscarCODIGO_Libro(codigo)
    if libro:
        return render_template('buscarcod.html', libro=libro)
    else:
        return jsonify({'Advertencia':'No se encuentra libro por codigo'})

@app.route('/buscaraut/<string:autor>', methods = ['GET'])
def buscar_autor(autor):
    libros = bibliotecaDB.buscarAUTOR_Libro(autor)
    if libros:
        return render_template('buscaraut.html', libros=libros)
    else:
        return jsonify({'Advertencia':'No se encuentra libro por autor'})

#-----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
