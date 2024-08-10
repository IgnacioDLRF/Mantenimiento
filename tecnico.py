from database import get_db_connection  # Asegúrate de importar get_db_connection

class Tecnico:
    def __init__(self, id, nombre, especialidad):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad

    def save(self, conn):
        cursor = conn.cursor()
        if self.id:
            cursor.execute('''
                UPDATE tecnico SET nombre = %s, especialidad = %s
                WHERE id = %s
            ''', (self.nombre, self.especialidad, self.id))
        else:
            cursor.execute('''
                INSERT INTO tecnico (nombre, especialidad) VALUES (%s, %s)
            ''', (self.nombre, self.especialidad))
            self.id = cursor.lastrowid
        conn.commit()
        cursor.close()

    def get_tareas(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, descripcion, fecha
            FROM tareasmantenimiento
            WHERE tecnico_id = %s
        ''', (self.id,))
        tareas = cursor.fetchall()
        cursor.close()
        return tareas

    def display_tareas(self, conn):
        tareas = self.get_tareas(conn)
        if tareas:
            for tarea in tareas:
                print(f"ID: {tarea[0]}, Descripción: {tarea[1]}, Fecha: {tarea[2]}")
        else:
            print("No hay tareas asignadas a este técnico.")

# Ejemplo de uso
if __name__ == "__main__":
    conn = get_db_connection()  # Asegúrate de que esta función esté definida para obtener la conexión a la base de datos
    tecnico = Tecnico(1, 'Juan Perez', 'Electricidad')
    tecnico.display_tareas(conn)
    conn.close()

