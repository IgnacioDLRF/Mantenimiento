import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk  # Asegurarse de que ttk esté importado
from request_controller import RequestController
from report_controller import ReportController
from new_report_view import NewReportView
from view_reports import ViewReports
from tecnico import Tecnico
from usuario import Usuario
from database import get_db_connection

class AdminView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Panel de Administración - {user['nombre']}")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")

        # Estilo
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=14)
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_color = "#2980b9"
        self.button_fg_color = "#ecf0f1"
        self.label_color = "#ecf0f1"

        # Título
        tk.Label(self.root, text=f"Panel de Administración - {user['nombre']}", font=self.title_font, bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

        # Botones para navegar entre secciones
        tk.Button(self.root, text="Ver Solicitudes", command=self.view_requests, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=10)
        tk.Button(self.root, text="Ver Reportes", command=self.view_reports, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=10)
        tk.Button(self.root, text="Añadir Técnico", command=self.add_tecnico, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=10)
        tk.Button(self.root, text="Añadir Usuario", command=self.add_usuario, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=10)
        if self.user['rol'] != 'técnico':
            tk.Button(self.root, text="Nuevo Reporte", command=self.new_report, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=10)

    def view_requests(self):
        controller = RequestController()
        solicitudes = controller.get_all_requests()
        request_window = tk.Toplevel(self.root)
        request_window.title("Solicitudes")
        request_window.geometry("800x400")
        request_window.configure(bg="#34495e")

        for solicitud in solicitudes:
            tk.Label(request_window, text=f"Descripción: {solicitud['descripcion']}, Fecha: {solicitud['fecha']}, Técnico ID: {solicitud['tecnico_id']}", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=5)
            tk.Button(request_window, text="Eliminar", command=lambda s_id=solicitud['id']: self.delete_request(s_id), bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=5)

    def view_reports(self):
        view_reports_window = tk.Toplevel(self.root)
        view_reports_window.configure(bg="#34495e")
        ViewReports(view_reports_window, self.user)

    def add_tecnico(self):
        add_tecnico_window = tk.Toplevel(self.root)
        add_tecnico_window.title("Añadir Técnico")
        add_tecnico_window.geometry("400x300")
        add_tecnico_window.configure(bg="#34495e")

        tk.Label(add_tecnico_window, text="Nombre", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=10)
        nombre_entry = tk.Entry(add_tecnico_window, font=self.label_font)
        nombre_entry.pack(pady=5)

        tk.Label(add_tecnico_window, text="Especialidad", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=10)
        especialidad_entry = tk.Entry(add_tecnico_window, font=self.label_font)
        especialidad_entry.pack(pady=5)

        def save_tecnico():
            nombre = nombre_entry.get()
            especialidad = especialidad_entry.get()
            conn = get_db_connection()
            tecnico = Tecnico(None, nombre, especialidad)
            tecnico.save(conn)
            conn.close()
            messagebox.showinfo("Éxito", "Técnico añadido exitosamente")
            add_tecnico_window.destroy()

        tk.Button(add_tecnico_window, text="Guardar", command=save_tecnico, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=20)

    def add_usuario(self):
        add_usuario_window = tk.Toplevel(self.root)
        add_usuario_window.title("Añadir Usuario")
        add_usuario_window.geometry("400x400")
        add_usuario_window.configure(bg="#34495e")

        tk.Label(add_usuario_window, text="Nombre", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=10)
        nombre_entry = tk.Entry(add_usuario_window, font=self.label_font)
        nombre_entry.pack(pady=5)

        tk.Label(add_usuario_window, text="Rol", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=10)
        rol_entry = tk.Entry(add_usuario_window, font=self.label_font)
        rol_entry.pack(pady=5)

        tk.Label(add_usuario_window, text="Correo", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=10)
        correo_entry = tk.Entry(add_usuario_window, font=self.label_font)
        correo_entry.pack(pady=5)

        tk.Label(add_usuario_window, text="Contraseña", bg="#34495e", fg="#ecf0f1", font=self.label_font).pack(pady=10)
        contrasena_entry = tk.Entry(add_usuario_window, font=self.label_font, show="*")
        contrasena_entry.pack(pady=5)

        def save_usuario():
            nombre = nombre_entry.get()
            rol = rol_entry.get()
            correo = correo_entry.get()
            contrasena = contrasena_entry.get()
            conn = get_db_connection()
            usuario = Usuario(None, nombre, rol, correo, contrasena)
            usuario.save(conn)
            conn.close()
            messagebox.showinfo("Éxito", "Usuario añadido exitosamente")
            add_usuario_window.destroy()

        tk.Button(add_usuario_window, text="Guardar", command=save_usuario, bg=self.button_color, fg=self.button_fg_color, font=self.button_font).pack(pady=20)

    def new_report(self):
        new_report_window = tk.Toplevel(self.root)
        NewReportView(new_report_window)

    def delete_request(self, request_id):
        controller = RequestController()
        controller.delete_request(request_id)
        messagebox.showinfo("Éxito", "Solicitud eliminada exitosamente")

    def delete_report(self, report_id):
        controller = ReportController()
        controller.delete_report(report_id)
        messagebox.showinfo("Éxito", "Reporte eliminado exitosamente")

# Código para inicializar la ventana principal y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    user = {'nombre': 'Admin', 'rol': 'administrador'}  # Ejemplo de usuario
    app = AdminView(root, user)
    root.mainloop()
