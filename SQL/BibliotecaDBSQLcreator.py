"""
Este es un creador de base de datos
Por defecto creara la base "db_libromania"

El creador se insertara en el -constructor init- de "BibliotecaClassSQL.py"
se busca reducir la cantidad de lineas realizando este modulo.

Ir a la ultima linea y utilizar los valores configurados en sus PC
Ponele -play- y verifica si se creo en tu propia consola o GUI dedicado (esto no se importa solo la funcion)
"""

import mysql.connector

#Los argumentos vendran de la API 
# Ver archivo "CRUD_Flask.py"
 
def creatorDBsql(host,user,password):
    
    print()
    print("-"*30,"\n")
    print("Creacion de base de datos 'db_libromania'.\n")
    print("-"*30,"\n")

    # Conexion a MySQL - Creacion de cursor
    conex = mysql.connector.connect(
        host = host,
        user = user, 
        password = password
    )

    cursor = conex.cursor()

    # Creacion de base "db_libromania"
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS db_libromania")
    print("Base de datos 'db_libromania' creada.\n")

    # Conexion a la base "db_libromania"
    conex = mysql.connector.connect(
        host = host,
        user = user, 
        password = password,
        database = 'db_libromania'
    )

    cursor = conex.cursor()

    # Creacion tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
        codigo INT AUTO_INCREMENT PRIMARY KEY,
        autor VARCHAR(255) NOT NULL,
        titulo VARCHAR(255) NOT NULL,
        portada VARCHAR(255)
        )
    """)
    print("Tabla 'libros' creada.\n")

    # Insercion libros por defecto y cambio el tipo de formato de la tabla

    libros_test = [
        ('Gabriel García Márquez', 'Cien años de soledad', './static/img/noimage.png'),
        ('J.K. Rowling', 'Harry Potter y la piedra filosofal', './static/img/noimage.png'),
        ('F. Scott Fitzgerald', 'El gran Gatsby', './static/img/noimage.png'),
        ('River Plate', 'La caída en la B', './static/img/noimage.png'),
        ('Jorge Luis Borges', 'Ficciones', './static/img/noimage.png'),
        ('Jane Austen', 'Orgullo y prejuicio', './static/img/noimage.png'),
        ('Haruki Murakami', 'Norwegian Wood', './static/img/noimage.png'),
        ('Ernest Hemingway', 'El viejo y el mar', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'El horror de Dunwich', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'La llamada de Cthulhu', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'En las montañas de la locura', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'El color que cayó del cielo', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'Los mitos de Cthulhu', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'La sombra sobre Innsmouth', './static/img/noimage.png'),
        ('H.P. Lovecraft', 'El caso de Charles Dexter Ward', './static/img/noimage.png'),
    ]

    insql = "INSERT INTO libros (autor, titulo, portada) VALUES (%s, %s, %s)"
    cursor.executemany(insql,libros_test)
    conex.commit()
    
    print("Libros por defecto insertados.\n")
    print("-"*30,"\n")    

    # Cierre conexiones provisorias
    cursor.close()
    conex.close()


"""
creatorDBsql("localhost","root","0000")
"""
