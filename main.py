# main.py

import tkinter as tk
from login import LoginView
from database import initialize_db

def main():
    initialize_db()
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()

if __name__ == '__main__':
    main()

