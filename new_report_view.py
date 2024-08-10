import tkinter as tk
from tkinter import messagebox, ttk
from database import get_db_connection
from solicitud import Solicitud
import datetime

class NewReportView:
    def __init__(self, root):
        self.root = root
        self.root.title("Generar Nuevo Reporte")
        self.root.geometry("400x300")  # Ajustar el tamaño de la ventana

        # Etiqueta y entrada para la descripción del reporte
        tk.Label(self.root, text="Descripción", font=("Arial", 12)).pack(pady=10)
        self.descripcion_entry = tk.Entry(self.root, font=("Arial", 12))
        self.descripcion_entry.pack(pady=5)

        # Selección de técnico
        tk.Label(self.root, text="Seleccionar Técnico", font=("Arial", 12)).pack(pady=10)
        self.tecnico_combo = ttk.Combobox(self.root, font=("Arial", 12))
        self.load_tecnicos()
        self.tecnico_combo.pack(pady=5)

        # Botón para generar el reporte
        tk.Button(self.root, text="Guardar", command=self.generate_report, font=("Arial", 12)).pack(pady=20)

    def load_tecnicos(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usuario_id, nombre FROM Usuarios WHERE rol = 'técnico'")
        tecnicos = cursor.fetchall()
        cursor.close()
        conn.close()
        self.tecnico_combo['values'] = [f"{tecnico['usuario_id']} - {tecnico['nombre']}" for tecnico in tecnicos]

    def generate_report(self):
        descripcion = self.descripcion_entry.get()
        tecnico_info = self.tecnico_combo.get()
        fecha_generacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not descripcion or not tecnico_info:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        tecnico_id = int(tecnico_info.split(" - ")[0])

        # Crear una nueva solicitud
        conn = get_db_connection()
        nueva_solicitud = Solicitud(None, descripcion, fecha_generacion, tecnico_id)
        nueva_solicitud.save(conn)
        conn.close()
        
        messagebox.showinfo("Éxito", "Reporte generado y técnico asignado exitosamente")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewReportView(root)
    root.mainloop()
