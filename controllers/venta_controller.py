"""
Controlador para gestionar ventas
"""
from models.venta import Venta
from models.producto import Producto


class VentaController:
    """Controlador para operaciones de ventas"""
    
    @staticmethod
    def crear_venta(producto_id, cantidad, precio_unitario):
        """Crea una nueva venta"""
        try:
            # Validaciones
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            if precio_unitario <= 0:
                raise ValueError("El precio unitario debe ser mayor a 0")
            
            # Verificar que el producto existe y tiene suficiente stock
            producto = Producto.obtener_por_id(producto_id)
            if not producto:
                raise ValueError("El producto no existe")
            if producto.cantidad_stock < cantidad:
                raise ValueError(f"Stock insuficiente. Disponible: {producto.cantidad_stock}")
            
            # Crear la venta
            venta_id = Venta.crear(producto_id, cantidad, precio_unitario)
            
            # Actualizar el stock del producto
            nuevo_stock = producto.cantidad_stock - cantidad
            Producto.actualizar(
                producto_id,
                producto.codigo,
                producto.nombre,
                producto.precio,
                nuevo_stock,
                producto.descripcion
            )
            
            return {"exito": True, "mensaje": "Venta registrada correctamente", "id": venta_id}
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al registrar la venta: {str(e)}"}
    
    @staticmethod
    def obtener_todas_ventas():
        """Obtiene todas las ventas"""
        try:
            ventas = Venta.obtener_todas()
            return {"exito": True, "datos": ventas}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al obtener ventas: {str(e)}"}
    
    @staticmethod
    def obtener_venta(venta_id):
        """Obtiene una venta por ID"""
        try:
            venta = Venta.obtener_por_id(venta_id)
            if venta:
                return {"exito": True, "datos": venta}
            else:
                return {"exito": False, "mensaje": "Venta no encontrada"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al obtener la venta: {str(e)}"}
    
    @staticmethod
    def actualizar_venta(venta_id, cantidad, precio_unitario):
        """Actualiza una venta existente"""
        try:
            # Validaciones
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            if precio_unitario <= 0:
                raise ValueError("El precio unitario debe ser mayor a 0")
            
            exito = Venta.actualizar(venta_id, cantidad, precio_unitario)
            if exito:
                return {"exito": True, "mensaje": "Venta actualizada correctamente"}
            else:
                return {"exito": False, "mensaje": "No se pudo actualizar la venta"}
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al actualizar la venta: {str(e)}"}
    
    @staticmethod
    def eliminar_venta(venta_id):
        """Elimina una venta y revierte el stock"""
        try:
            # Obtener los datos de la venta
            venta = Venta.obtener_por_id(venta_id)
            if not venta:
                raise ValueError("Venta no encontrada")
            
            # Obtener el producto
            producto = Producto.obtener_por_id(venta['producto_id'])
            if not producto:
                raise ValueError("Producto no encontrado")
            
            # Revertir el stock
            nuevo_stock = producto.cantidad_stock + venta['cantidad']
            Producto.actualizar(
                producto.id,
                producto.codigo,
                producto.nombre,
                producto.precio,
                nuevo_stock,
                producto.descripcion
            )
            
            # Eliminar la venta
            exito = Venta.eliminar(venta_id)
            if exito:
                return {"exito": True, "mensaje": "Venta eliminada correctamente"}
            else:
                return {"exito": False, "mensaje": "No se pudo eliminar la venta"}
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al eliminar la venta: {str(e)}"}
    
    @staticmethod
    def obtener_total_ventas():
        """Obtiene el total de ventas"""
        try:
            total = Venta.obtener_total_ventas()
            return {"exito": True, "datos": total}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al calcular el total de ventas: {str(e)}"}
