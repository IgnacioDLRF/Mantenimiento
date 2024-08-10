# maintenance_controller.py

from database import get_db_connection

class MaintenanceController:
    def __init__(self):
        pass

    def schedule_maintenance(self, report_id, descripcion, tecnico_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO TareasMantenimiento (solicitud_id, tecnico_id, descripcion, fecha_asignacion, estado)
            VALUES (%s, %s, %s, CURDATE(), 'en progreso')
        ''', (report_id, tecnico_id, descripcion))
        
        conn.commit()
        cursor.close()
        conn.close()
