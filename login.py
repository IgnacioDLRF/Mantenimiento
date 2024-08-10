import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importar PIL para cargar la imagen
from admin_view import AdminView
from technician_view import TechnicianView
from database import get_db_connection

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x400")  # Ajusta el tamaño de la ventana aquí

        # Cargar y mostrar la imagen
        image_path = "C:\\Users\\antic\\OneDrive\\Escritorio\\UACH\\Materias\\07-Cuatrimestre_Enero-Abril_2024\\Proyectos profesionales 2\\Mantenimiento_Ind\\mantenimiento.png"
        self.img = Image.open(image_path)
        self.img = self.img.resize((150, 150), Image.LANCZOS)  # Ajustar el tamaño de la imagen
        self.img = ImageTk.PhotoImage(self.img)
        tk.Label(self.root, image=self.img).pack(pady=10)

        # Etiqueta y entrada para el nombre de usuario
        tk.Label(self.root, text="Usuario", font=("Arial", 12), bg="#ffffff", fg="#000000").pack(pady=10)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), bg="#f0f0f0", fg="#000000")
        self.username_entry.pack(pady=5)

        # Etiqueta y entrada para la contraseña
        tk.Label(self.root, text="Contraseña", font=("Arial", 12), bg="#ffffff", fg="#000000").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), bg="#f0f0f0", fg="#000000")
        self.password_entry.pack(pady=5)

        # Botón de login
        tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12), bg="#007acc", fg="#ffffff").pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM Usuarios WHERE nombre = %s AND contraseña = %s', (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            messagebox.showinfo("Éxito", "Login exitoso")
            self.root.destroy()
            if user['rol'] == 'técnico':
                root = tk.Tk()
                app = TechnicianView(root, user)
            else:
                root = tk.Tk()
                app = AdminView(root, user)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()
