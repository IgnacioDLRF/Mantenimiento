# solicitud.py

class Solicitud:
    def __init__(self, id, descripcion, fecha, tecnico_id):
        self.id = id
        self.descripcion = descripcion
        self.fecha = fecha
        self.tecnico_id = tecnico_id

    def save(self, conn):
        cursor = conn.cursor()
        if self.id:
            cursor.execute('''
                UPDATE solicitud SET descripcion = %s, fecha = %s, tecnico_id = %s
                WHERE id = %s
            ''', (self.descripcion, self.fecha, self.tecnico_id, self.id))
        else:
            cursor.execute('''
                INSERT INTO solicitud (descripcion, fecha, tecnico_id) VALUES (%s, %s, %s)
            ''', (self.descripcion, self.fecha, self.tecnico_id))
            self.id = cursor.lastrowid
        conn.commit()
        cursor.close()
