# usuario.py

class Usuario:
    def __init__(self, id, nombre, rol, correo, contrasena):
        self.id = id
        self.nombre = nombre
        self.rol = rol
        self.correo = correo
        self.contrasena = contrasena

    def save(self, conn):
        cursor = conn.cursor()
        if self.id:
            cursor.execute('''
                UPDATE usuario SET nombre = %s, rol = %s, correo = %s, contrasena = %s
                WHERE id = %s
            ''', (self.nombre, self.rol, self.correo, self.contrasena, self.id))
        else:
            cursor.execute('''
                INSERT INTO usuario (nombre, rol, correo, contrasena) VALUES (%s, %s, %s, %s)
            ''', (self.nombre, self.rol, self.correo, self.contrasena))
            self.id = cursor.lastrowid
        conn.commit()
        cursor.close()
