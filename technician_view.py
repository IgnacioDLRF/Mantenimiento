# technician_view.py

import tkinter as tk
from tkinter import font
from request_controller import RequestController
from view_reports import ViewReports
from database import get_db_connection

class TechnicianView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Panel de Técnico - {user['nombre']}")
        self.root.geometry("600x300")  # Ajusta el tamaño de la ventana aquí
        self.root.configure(bg="#2c3e50")

        # Estilo
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=14)
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_color = "#2980b9"
        self.button_fg_color = "#ecf0f1"
        self.label_color = "#ecf0f1"

        # Título
        tk.Label(self.root, text=f"Panel de Técnico - {user['nombre']}", font=self.title_font, bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

        # Botones para navegar entre secciones
        tk.Button(self.root, text="Ver Reportes", command=self.view_reports, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=10)

        # Mostrar las solicitudes asignadas al técnico por defecto
        self.show_assigned_requests()

    def show_assigned_requests(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT id, descripcion, fecha_asignacion, estado
            FROM TareasMantenimiento
            WHERE tecnico_id = %s
        ''', (self.user['id'],))
        solicitudes = cursor.fetchall()
        cursor.close()
        conn.close()

        request_window = tk.Frame(self.root, bg="#2c3e50")
        request_window.pack(pady=20)

        for solicitud in solicitudes:
            tk.Label(request_window, text=f"ID: {solicitud['id']}, Descripción: {solicitud['descripcion']}, Fecha: {solicitud['fecha_asignacion']}, Estado: {solicitud['estado']}", bg="#2c3e50", fg="#ecf0f1", font=self.label_font).pack(pady=5)

    def view_reports(self):
        view_reports_window = tk.Toplevel(self.root)
        view_reports_window.configure(bg="#34495e")
        ViewReports(view_reports_window, self.user)

if __name__ == "__main__":
    root = tk.Tk()
    user = {'id': 1, 'nombre': 'Técnico de Prueba', 'rol': 'técnico'}  # Ejemplo de usuario
    app = TechnicianView(root, user)
    root.mainloop()
