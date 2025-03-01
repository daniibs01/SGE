import sqlite3

def crear_base_de_datos():
    # Nombre del archivo de la base de datos
    nombre_bd = "Gestor.db"

    # Conectar a la base de datos (se crea si no existe)
    conexion = sqlite3.connect(nombre_bd)
    cursor = conexion.cursor()

    # Crear la tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL,
        administrador BOOLEAN NOT NULL
    )
    ''')

    # Insertar un usuario administrador y uno no administrador
    roles_iniciales = [
        ("admin", "admin", True),  # Usuario administrador
        ("usuario", "usuario", False)  # Usuario no administrador
    ]

    # Insertar usuarios si no existen
    for usuario, contrasena, administrador in roles_iniciales:
        cursor.execute('''
        INSERT OR IGNORE INTO usuarios (usuario, contrasena, administrador)
        VALUES (?, ?, ?)
        ''', (usuario, contrasena, administrador))

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

    print(f"Base de datos '{nombre_bd}' creada con éxito y usuarios iniciales añadidos.")

# Llamar a la función para crear la base de datos
if __name__ == "__main__":
    crear_base_de_datos()