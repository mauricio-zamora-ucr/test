"""
Modelos de datos para Venta
"""
from database.connection import DatabaseConnection
import sqlite3


class Venta:
    """Modelo para gestionar ventas"""
    
    def __init__(self, producto_id, cantidad, precio_unitario, venta_id=None):
        self.id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario
        self.fecha_venta = None
    
    @staticmethod
    def crear(producto_id, cantidad, precio_unitario):
        """Crea una nueva venta en la base de datos"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        subtotal = cantidad * precio_unitario
        
        try:
            cursor.execute('''
                INSERT INTO ventas (producto_id, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?)
            ''', (producto_id, cantidad, precio_unitario, subtotal))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            raise ValueError(f"Error al registrar la venta: {e}")
    
    @staticmethod
    def obtener_todas():
        """Obtiene todas las ventas con información del producto"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, p.codigo, p.nombre 
            FROM ventas v
            LEFT JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha_venta DESC
        ''')
        rows = cursor.fetchall()
        
        ventas = []
        for row in rows:
            venta = {
                'id': row['id'],
                'producto_id': row['producto_id'],
                'codigo_producto': row['codigo'],
                'nombre_producto': row['nombre'],
                'cantidad': row['cantidad'],
                'precio_unitario': row['precio_unitario'],
                'subtotal': row['subtotal'],
                'fecha_venta': row['fecha_venta']
            }
            ventas.append(venta)
        
        return ventas
    
    @staticmethod
    def obtener_por_id(venta_id):
        """Obtiene una venta por su ID"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, p.codigo, p.nombre 
            FROM ventas v
            LEFT JOIN productos p ON v.producto_id = p.id
            WHERE v.id = ?
        ''', (venta_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row['id'],
                'producto_id': row['producto_id'],
                'codigo_producto': row['codigo'],
                'nombre_producto': row['nombre'],
                'cantidad': row['cantidad'],
                'precio_unitario': row['precio_unitario'],
                'subtotal': row['subtotal'],
                'fecha_venta': row['fecha_venta']
            }
        
        return None
    
    @staticmethod
    def actualizar(venta_id, cantidad, precio_unitario):
        """Actualiza una venta existente"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        subtotal = cantidad * precio_unitario
        
        try:
            cursor.execute('''
                UPDATE ventas 
                SET cantidad = ?, precio_unitario = ?, subtotal = ?
                WHERE id = ?
            ''', (cantidad, precio_unitario, subtotal, venta_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            raise ValueError(f"Error al actualizar la venta: {e}")
    
    @staticmethod
    def eliminar(venta_id):
        """Elimina una venta"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM ventas WHERE id = ?', (venta_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def obtener_total_ventas():
        """Obtiene el total de ventas"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(subtotal) as total FROM ventas')
        row = cursor.fetchone()
        
        return row['total'] or 0
