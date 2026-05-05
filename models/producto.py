"""
Modelos de datos para Producto
"""
from database.connection import DatabaseConnection
from datetime import datetime


class Producto:
    """Modelo para gestionar productos"""
    
    def __init__(self, codigo, nombre, precio, cantidad_stock, descripcion="", producto_id=None):
        self.id = producto_id
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad_stock = cantidad_stock
        self.fecha_creacion = None
        self.fecha_actualizacion = None
    
    @staticmethod
    def crear(codigo, nombre, precio, cantidad_stock, descripcion=""):
        """Crea un nuevo producto en la base de datos"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, descripcion, precio, cantidad_stock)
                VALUES (?, ?, ?, ?, ?)
            ''', (codigo, nombre, descripcion, precio, cantidad_stock))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"El código del producto ya existe: {e}")
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        
        productos = []
        for row in rows:
            producto = Producto(
                codigo=row['codigo'],
                nombre=row['nombre'],
                precio=row['precio'],
                cantidad_stock=row['cantidad_stock'],
                descripcion=row['descripcion'],
                producto_id=row['id']
            )
            producto.fecha_creacion = row['fecha_creacion']
            producto.fecha_actualizacion = row['fecha_actualizacion']
            productos.append(producto)
        
        return productos
    
    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por su ID"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        row = cursor.fetchone()
        
        if row:
            producto = Producto(
                codigo=row['codigo'],
                nombre=row['nombre'],
                precio=row['precio'],
                cantidad_stock=row['cantidad_stock'],
                descripcion=row['descripcion'],
                producto_id=row['id']
            )
            producto.fecha_creacion = row['fecha_creacion']
            producto.fecha_actualizacion = row['fecha_actualizacion']
            return producto
        
        return None
    
    @staticmethod
    def actualizar(producto_id, codigo, nombre, precio, cantidad_stock, descripcion=""):
        """Actualiza un producto existente"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE productos 
                SET codigo = ?, nombre = ?, descripcion = ?, precio = ?, cantidad_stock = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (codigo, nombre, descripcion, precio, cantidad_stock, producto_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            raise ValueError(f"El código del producto ya existe: {e}")
    
    @staticmethod
    def eliminar(producto_id):
        """Elimina un producto"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def obtener_por_codigo(codigo):
        """Obtiene un producto por su código"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()
        
        if row:
            return row['id']
        return None


import sqlite3
