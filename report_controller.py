# report_controller.py

from database import get_db_connection

class ReportController:
    def __init__(self):
        pass

    def get_all_reports(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Reportes')
        reportes = cursor.fetchall()
        cursor.close()
        conn.close()
        return reportes

    def create_report(self, tipo_reporte, contenido, fecha_generacion):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Reportes (tipo_reporte, fecha_generacion, contenido)
            VALUES (%s, %s, %s)
        ''', (tipo_reporte, fecha_generacion, contenido))
        
        report_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return report_id

    def delete_report(self, report_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM Reportes WHERE reporte_id = %s', (report_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
