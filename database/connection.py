import sqlite3
import os
from config.settings import DATABASE_PATH, DATA_DIR


class DatabaseConnection:
    """Gestiona la conexión a la base de datos SQLite"""
    
    _connection = None
    
    @staticmethod
    def get_connection():
        """Obtiene la conexión a la base de datos"""
        if DatabaseConnection._connection is None:
            os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
            DatabaseConnection._connection = sqlite3.connect(DATABASE_PATH)
            DatabaseConnection._connection.row_factory = sqlite3.Row
        return DatabaseConnection._connection
    
    @staticmethod
    def close_connection():
        """Cierra la conexión a la base de datos"""
        if DatabaseConnection._connection is not None:
            DatabaseConnection._connection.close()
            DatabaseConnection._connection = None
    
    @staticmethod
    def create_tables():
        """Crea las tablas necesarias en la base de datos"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad_stock INTEGER NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        
        conn.commit()
