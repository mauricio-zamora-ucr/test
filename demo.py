"""
Script de demostración con datos de prueba
Este script crea algunos productos y ventas de ejemplo para probar la aplicación
"""
from database.connection import DatabaseConnection
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController


def main():
    """Crea datos de ejemplo"""
    print("Inicializando base de datos...")
    DatabaseConnection.create_tables()
    
    print("\nCreando productos de ejemplo...")
    
    # Crear algunos productos
    productos_datos = [
        ("LAPTOP001", "Laptop HP 15.6\"", 899.99, 10, "Laptop HP 15.6 pulgadas, Intel i5, 8GB RAM"),
        ("MOUSE001", "Mouse Inalámbrico", 29.99, 50, "Mouse inalámbrico Logitech MX Master 3"),
        ("TECLADO001", "Teclado Mecánico RGB", 149.99, 25, "Teclado mecánico RGB Cherry MX"),
        ("MONITOR001", "Monitor LG 27\" 4K", 399.99, 5, "Monitor LG UltraFine 27\" 4K IPS"),
        ("CABLE001", "Cable HDMI 2.0", 15.99, 100, "Cable HDMI 2.0 de alta velocidad"),
        ("HEADSET001", "Headset Gaming", 79.99, 15, "Headset gaming inalámbrico RGB"),
    ]
    
    for codigo, nombre, precio, stock, descripcion in productos_datos:
        resultado = ProductoController.crear_producto(codigo, nombre, precio, stock, descripcion)
        if resultado['exito']:
            print(f"✓ {codigo}: {nombre} - ${precio}")
        else:
            print(f"✗ {codigo}: {resultado['mensaje']}")
    
    print("\nCreando ventas de ejemplo...")
    
    # Crear algunas ventas
    ventas_datos = [
        (1, 2, 899.99),  # Productos 1, cantidad 2
        (2, 5, 29.99),   # Mouse, cantidad 5
        (3, 1, 149.99),  # Teclado, cantidad 1
        (4, 1, 399.99),  # Monitor, cantidad 1
        (5, 10, 15.99),  # Cables, cantidad 10
    ]
    
    for producto_id, cantidad, precio in ventas_datos:
        resultado = VentaController.crear_venta(producto_id, cantidad, precio)
        if resultado['exito']:
            print(f"✓ Venta registrada: Producto {producto_id}, Cantidad {cantidad}")
        else:
            print(f"✗ Error en venta: {resultado['mensaje']}")
    
    print("\n✅ Datos de ejemplo creados exitosamente")
    print("\nAhora puedes ejecutar: python main.py")


if __name__ == "__main__":
    main()
