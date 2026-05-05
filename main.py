"""
Aplicación principal de Gestión de Productos y Ventas
Arquitectura MVC de N-capas con tkinter y SQLite
"""
import tkinter as tk
from database.connection import DatabaseConnection
from views.main_window import MainWindow
import sys


def main():
    """Función principal"""
    try:
        # Inicializar la base de datos
        DatabaseConnection.create_tables()
        
        # Crear la ventana principal
        root = tk.Tk()
        
        # Crear la interfaz
        app = MainWindow(root)
        
        # Configurar el cierre de la aplicación
        def on_closing():
            DatabaseConnection.close_connection()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Iniciar la aplicación
        root.mainloop()
    
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
