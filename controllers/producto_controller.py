"""
Controlador para gestionar productos
"""
from models.producto import Producto


class ProductoController:
    """Controlador para operaciones de productos"""
    
    @staticmethod
    def crear_producto(codigo, nombre, precio, cantidad_stock, descripcion=""):
        """Crea un nuevo producto"""
        try:
            # Validaciones
            if not codigo or not codigo.strip():
                raise ValueError("El código del producto es requerido")
            if not nombre or not nombre.strip():
                raise ValueError("El nombre del producto es requerido")
            if precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")
            if cantidad_stock < 0:
                raise ValueError("La cantidad de stock no puede ser negativa")
            
            producto_id = Producto.crear(codigo, nombre, precio, cantidad_stock, descripcion)
            return {"exito": True, "mensaje": "Producto creado correctamente", "id": producto_id}
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al crear el producto: {str(e)}"}
    
    @staticmethod
    def obtener_todos_productos():
        """Obtiene todos los productos"""
        try:
            productos = Producto.obtener_todos()
            return {"exito": True, "datos": productos}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al obtener productos: {str(e)}"}
    
    @staticmethod
    def obtener_producto(producto_id):
        """Obtiene un producto por ID"""
        try:
            producto = Producto.obtener_por_id(producto_id)
            if producto:
                return {"exito": True, "datos": producto}
            else:
                return {"exito": False, "mensaje": "Producto no encontrado"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al obtener el producto: {str(e)}"}
    
    @staticmethod
    def actualizar_producto(producto_id, codigo, nombre, precio, cantidad_stock, descripcion=""):
        """Actualiza un producto existente"""
        try:
            # Validaciones
            if not codigo or not codigo.strip():
                raise ValueError("El código del producto es requerido")
            if not nombre or not nombre.strip():
                raise ValueError("El nombre del producto es requerido")
            if precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")
            if cantidad_stock < 0:
                raise ValueError("La cantidad de stock no puede ser negativa")
            
            exito = Producto.actualizar(producto_id, codigo, nombre, precio, cantidad_stock, descripcion)
            if exito:
                return {"exito": True, "mensaje": "Producto actualizado correctamente"}
            else:
                return {"exito": False, "mensaje": "No se pudo actualizar el producto"}
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al actualizar el producto: {str(e)}"}
    
    @staticmethod
    def eliminar_producto(producto_id):
        """Elimina un producto"""
        try:
            exito = Producto.eliminar(producto_id)
            if exito:
                return {"exito": True, "mensaje": "Producto eliminado correctamente"}
            else:
                return {"exito": False, "mensaje": "No se pudo eliminar el producto"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al eliminar el producto: {str(e)}"}
