# database.py

import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user='root', 
            password='860513',
            host='localhost',
            database='mantenimiento'
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
        return None

def initialize_db():
    conn = get_db_connection()
    if conn is None:
        print("Error: No se pudo establecer conexión con la base de datos")
        return
    
    cursor = conn.cursor()
    
    # Creación de las tablas
    tables = {
        "Usuarios": """
            CREATE TABLE IF NOT EXISTS Usuarios (
                usuario_id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(255) NOT NULL,
                rol ENUM('técnico', 'supervisor', 'administrador', 'cliente') NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                contraseña VARCHAR(255) NOT NULL
            )
        """,
        "SolicitudesMantenimiento": """
            CREATE TABLE IF NOT EXISTS SolicitudesMantenimiento (
                solicitud_id INT PRIMARY KEY AUTO_INCREMENT,
                cliente_id INT,
                descripcion TEXT NOT NULL,
                fecha_creacion DATETIME NOT NULL,
                estado ENUM('pendiente', 'en progreso', 'completado') NOT NULL,
                prioridad ENUM('baja', 'media', 'alta') NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES Usuarios(usuario_id)
            )
        """,
        "TareasMantenimiento": """
            CREATE TABLE IF NOT EXISTS TareasMantenimiento (
                tarea_id INT PRIMARY KEY AUTO_INCREMENT,
                solicitud_id INT,
                tecnico_id INT,
                descripcion TEXT NOT NULL,
                fecha_asignacion DATETIME NOT NULL,
                fecha_completado DATETIME,
                estado ENUM('pendiente', 'en progreso', 'completado') NOT NULL,
                FOREIGN KEY (solicitud_id) REFERENCES SolicitudesMantenimiento(solicitud_id),
                FOREIGN KEY (tecnico_id) REFERENCES Usuarios(usuario_id)
            )
        """,
        "HistorialMantenimiento": """
            CREATE TABLE IF NOT EXISTS HistorialMantenimiento (
                historial_id INT PRIMARY KEY AUTO_INCREMENT,
                tarea_id INT,
                fecha DATETIME NOT NULL,
                observaciones TEXT,
                FOREIGN KEY (tarea_id) REFERENCES TareasMantenimiento(tarea_id)
            )
        """,
        "InventarioRepuestos": """
            CREATE TABLE IF NOT EXISTS InventarioRepuestos (
                repuesto_id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(255) NOT NULL,
                cantidad_disponible INT NOT NULL,
                ubicacion VARCHAR(255),
                proveedor VARCHAR(255)
            )
        """,
        "Reportes": """
            CREATE TABLE IF NOT EXISTS Reportes (
                reporte_id INT PRIMARY KEY AUTO_INCREMENT,
                tipo_reporte VARCHAR(255) NOT NULL,
                fecha_generacion DATETIME NOT NULL,
                contenido TEXT
            )
        """
    }

    # Ejecución de la creación de tablas
    for table_name, table_sql in tables.items():
        cursor.execute(table_sql)
        print(f"Tabla '{table_name}' creada exitosamente")

    # Confirmar cambios y cerrar la conexión
    conn.commit()
    cursor.close()
    conn.close()
    print("Conexión cerrada")

if __name__ == "__main__":
    initialize_db()
