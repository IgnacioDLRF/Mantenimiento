# view_reports.py

import tkinter as tk
from tkinter import messagebox
from database import get_db_connection
from report_controller import ReportController

class ViewReports:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Ver Reportes")
        self.root.geometry("600x400")

        self.report_listbox = tk.Listbox(self.root, font=("Arial", 12), width=80)
        self.report_listbox.pack(pady=20)

        if user['rol'] != 'técnico':
            tk.Button(self.root, text="Asignar Técnico", command=self.assign_technician, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Marcar como Resuelto", command=self.resolve_report, font=("Arial", 12)).pack(pady=10)

        self.load_reports()

    def load_reports(self):
        controller = ReportController()
        self.reports = controller.get_all_reports()

        for report in self.reports:
            tecnico_id = report['tecnico_id'] if report['tecnico_id'] else "No asignado"
            self.report_listbox.insert(tk.END, f"ID: {report['reporte_id']}, Tipo: {report['tipo_reporte']}, Fecha: {report['fecha_generacion']}, Técnico: {tecnico_id}, Estado: {report['estado']}")

    def assign_technician(self):
        selected_index = self.report_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Seleccione un reporte")
            return

        selected_report = self.reports[selected_index[0]]
        self.assign_technician_window(selected_report['reporte_id'])

    def assign_technician_window(self, report_id):
        assign_window = tk.Toplevel(self.root)
        assign_window.title("Asignar Técnico")
        assign_window.geometry("400x300")

        tk.Label(assign_window, text="Selecciona un Técnico", font=("Arial", 12)).pack(pady=10)
        self.technician_listbox = tk.Listbox(assign_window, font=("Arial", 12), width=50)
        self.technician_listbox.pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Usuarios WHERE rol = 'técnico'")
        self.technicians = cursor.fetchall()

        for technician in self.technicians:
            self.technician_listbox.insert(tk.END, f"ID: {technician['usuario_id']}, Nombre: {technician['nombre']}")

        cursor.close()
        conn.close()

        tk.Button(assign_window, text="Asignar", command=lambda: self.assign(report_id), font=("Arial", 12)).pack(pady=10)

    def assign(self, report_id):
        selected_index = self.technician_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Seleccione un técnico")
            return

        selected_technician = self.technicians[selected_index[0]]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Reportes SET tecnico_id = %s, estado = 'en progreso' WHERE reporte_id = %s", (selected_technician['usuario_id'], report_id))
        cursor.execute("INSERT INTO TareasMantenimiento (solicitud_id, tecnico_id, descripcion, fecha_asignacion, estado) VALUES (%s, %s, %s, CURDATE(), 'en progreso')", (report_id, selected_technician['usuario_id'], selected_technician['nombre']))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Éxito", "Técnico asignado exitosamente")
        self.root.destroy()

    def resolve_report(self):
        selected_index = self.report_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Seleccione un reporte")
            return

        selected_report = self.reports[selected_index[0]]

        if selected_report['estado'] != 'en progreso':
            messagebox.showerror("Error", "Solo se pueden resolver reportes en progreso")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TareasMantenimiento WHERE solicitud_id = %s", (selected_report['reporte_id'],))
        cursor.execute("DELETE FROM Reportes WHERE reporte_id = %s", (selected_report['reporte_id'],))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Éxito", "Reporte marcado como resuelto y eliminado")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    user = {'nombre': 'Usuario de Prueba', 'rol': 'administrador'}
    app = ViewReports(root, user)
    root.mainloop()
