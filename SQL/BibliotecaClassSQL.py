"""
Adaptacion de la clase "Biblioteca" con el conector MySQL para crear
los objetos "libro", para almacenar en el vector "Libros = []"
y luego aplicar en la API web

Faltan parametros que en la clase base si estan (BibliotecaClass.py)
Es mas corta, reducida a los siguientes parametros de libros:
- codigo - autor - titulo - portada
"""

"""
Se lista a continuacion los metodos para no estar buscando uno por uno:

# Constructor
def __init__(self,host,user,password,database):

# Nuevo libro - Metodo
def agregar_Libro(self,codigo,autor,titulo,portada):

    # Se tiene dos metodos para busqueda de libros
# Buscar libro codigo -Metodo
def buscarCODIGO_Libro(self,codigo):

# Buscar libro autor -Metodo
def buscarAUTOR_Libro(self,autor):

    # Se tienen dos metodos para eliminado de libros
# Eliminar libro codigo -Metodo
def eliminarCODIGO_Libro(self,codigo):

# Eliminar libro autor -Metodo (Eliminacion en masa)
def eliminarAUTOR_Libro(self,autor):
    
# Modificar libro -Metodo
def modificar_Libro(self,codigo,autor,titulo,portada):
    
# Mostrar libros - 1) Los datos de un libro 2) Toda la DB
def mostrarUNO_libro(self,codigo):
def mostrarTODOS_libro(self):
"""
import mysql.connector
from SQL.BibliotecaDBSQLcreator import creatorDBsql

urlIMG = "./static/img/noimage.png"

# Importante, se asume que la tabla (no la base) se llama "libros"
# Importante, se asume que la base se llame "db_libromania"

# Funciones de conexion
# Inicio Conexion a base de datos
def conec_db(host,user,password):
    conex = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='db_libromania'
    )
    cursor = conex.cursor(dictionary=True)
    return conex, cursor

# Fin Conexion a base de datos 
def disconect_db(conex,cursor):
    cursor.close()
    conex.close()

# Clase Biblioteca  - Base de datos SQL

class Biblioteca:

    # Constructor
    def __init__(self, host, user, password):
        
        self.host = host
        self.user = user
        self.password = password
        self.conex = None
        self.cursor = None
    
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            print("\n","Conexion exitosa a DB.")
            print("-"*30,"\n")

        except mysql.connector.Error as err:
            print(f"No es posible la conexion. Error: {err}")
            print("Se procede a crear una base de datos.")
            creatorDBsql(self.host,self.user,self.password)        
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)

            if self.cursor:
                print(f"\n","Conexion exitosa a DB.")
                print("-"*30,"")
            else:
                print(f"No es posible conectar a DB {err}")
                print("-"*30,"\n")
                return None
                    
    # Nuevo libro - Metodo
    def agregar_Libro(self,autor,titulo,portada = urlIMG):
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            insql = "INSERT INTO  libros (autor,titulo,portada) VALUES (%s,%s,%s)"
            inputLibro = (autor,titulo,portada)
            self.cursor.execute(insql,inputLibro)
            self.conex.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30,"\n")
            return None
        finally:
            disconect_db(self.conex,self.cursor)

    # Se tiene dos metodos para busqueda de libros
    # Buscar libro codigo -Metodo
    def buscarCODIGO_Libro(self, codigo):
        try:
            self.conex, self.cursor = conec_db(self.host, self.user, self.password)
            insql = "SELECT * FROM libros WHERE codigo = %s"
            self.cursor.execute(insql,(codigo,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30,"\n")
            return None
        finally:
            disconect_db(self.conex, self.cursor)
    
    # Buscar libro autor - Método
    def buscarAUTOR_Libro(self, autor):
        try:
            self.conex, self.cursor = conec_db(self.host, self.user, self.password)
            insql = "SELECT * FROM libros WHERE autor = %s"
            self.cursor.execute(insql, (autor,))           
            # Paso de tupla a diccionario
            libros = []
            for row in self.cursor.fetchall():
                libro = {
                    'codigo': row['codigo'],
                    'autor': row['autor'],
                    'titulo': row['titulo'],
                    'portada': row['portada']
                }
                libros.append(libro)
            return libros
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30, "\n")
            return None
        finally:
            disconect_db(self.conex, self.cursor)
        
    # Se tienen dos metodos para eliminado de libros
    # Eliminar libro codigo -Metodo
    def eliminarCODIGO_Libro(self,codigo):
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            insql = "DELETE FROM libros WHERE codigo = %s"
            self.cursor.execute(insql,(codigo,))
            self.conex.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30,"\n")
            return None
        finally:
            disconect_db(self.conex,self.cursor)

    # Eliminar libro autor -Metodo (Eliminacion en masa)
    def eliminarAUTOR_Libro(self,autor):
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            insql = "DELETE FROM libros WHERE autor = %s"
            self.cursor.execute(insql,(autor,))
            self.conex.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
                print(f"No es posible conectar a DB {err}")
                print("-"*30,"\n")
                return None
        finally:
            disconect_db(self.conex,self.cursor)

    # Modificar libro -Metodo
    def modificar_Libro(self,codigo,autor,titulo,portada):
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            insql = "UPDATE libros SET autor = %s, titulo = %s, portada = %s WHERE codigo = %s"
            actualizar = (autor,titulo,portada,codigo) 
            self.cursor.execute(insql,actualizar)
            self.conex.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30,"\n")
            return None
        finally:
            disconect_db(self.conex,self.cursor)        
    
    # Mostrar libros - 1) Los datos de un libro 2) Toda la DB
    def mostrarUNO_libro(self,codigo):
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            libro = self.buscarCODIGO_Libro(codigo)
            if libro:
                print("-" * 30)
                print("Datos solicitados")
                print("-" * 30)
                print(f"COD...... = {libro['codigo']}")
                print(f"AUTOR.... = {libro['autor']}")
                print(f"TITULO... = {libro['titulo']}")
                print(f"PORTADA.. = {libro['portada']}")
                print("-" * 30)
                print()
            else:
                print("Libro INEXISTENTE / NO encontrado.\n")
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30,"\n")
            return None
        finally:
            disconect_db(self.conex,self.cursor)    

    def mostrarTODOS_libro(self):
        try:
            self.conex, self.cursor = conec_db(self.host,self.user,self.password)
            insql = "SELECT * FROM libros"
            self.cursor.execute(insql)
            libros = self.cursor.fetchall()
            print(libros)
            return libros
        except mysql.connector.Error as err:
            print(f"No es posible conectar a DB {err}")
            print("-"*30,"\n")
            return None
        finally:
            disconect_db(self.conex,self.cursor)    
