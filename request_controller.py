# request_controller.py

from database import get_db_connection
from solicitud import Solicitud

class RequestController:
    def __init__(self):
        pass

    def get_all_requests(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitud')
        solicitudes = cursor.fetchall()
        cursor.close()
        conn.close()
        return solicitudes

    def create_request(self, descripcion, fecha, tecnico_id=None):
        conn = get_db_connection()
        solicitud = Solicitud(None, descripcion, fecha, tecnico_id)
        solicitud.save(conn)
        conn.close()
    
    def delete_request(self, request_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM solicitud WHERE id = %s', (request_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
