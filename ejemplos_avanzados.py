"""
Ejemplos avanzados de uso de la aplicación
Estos scripts muestran cómo usar la aplicación programáticamente
"""

# ==============================================================================
# EJEMPLO 1: Crear productos en lote
# ==============================================================================

def ejemplo_crear_productos_lote():
    """Crea múltiples productos de una sola vez"""
    from controllers.producto_controller import ProductoController
    
    productos = [
        ("SKU001", "IPhone 12", 799, 15, "Apple iPhone 12 64GB"),
        ("SKU002", "Samsung Galaxy S21", 899, 12, "Samsung Galaxy S21 128GB"),
        ("SKU003", "Pixel 6", 599, 20, "Google Pixel 6 128GB"),
        ("SKU004", "OnePlus 9", 729, 10, "OnePlus 9 128GB"),
    ]
    
    print("Creando productos en lote...")
    for prod_codigo, prod_nombre, precio, stock, descripcion in productos:
        resultado = ProductoController.crear_producto(
            prod_codigo, prod_nombre, precio, stock, descripcion
        )
        if resultado['exito']:
            print(f"✓ {prod_nombre} creado (ID: {resultado['id']})")
        else:
            print(f"✗ Error: {resultado['mensaje']}")


# ==============================================================================
# EJEMPLO 2: Generar reporte de ventas
# ==============================================================================

def ejemplo_reporte_ventas():
    """Genera un reporte de ventas total"""
    from controllers.venta_controller import VentaController
    from models.producto import Producto
    
    resultado_ventas = VentaController.obtener_todas_ventas()
    
    if resultado_ventas['exito']:
        ventas = resultado_ventas['datos']
        
        print("\\n" + "="*60)
        print("REPORTE DE VENTAS")
        print("="*60)
        
        total = 0
        for venta in ventas:
            print(f"ID: {venta['id']} | {venta['nombre_producto']}: "
                  f"{venta['cantidad']} x ${venta['precio_unitario']:.2f} = "
                  f"${venta['subtotal']:.2f}")
            total += venta['subtotal']
        
        print("="*60)
        print(f"TOTAL VENTAS: ${total:.2f}")
        print("="*60 + "\\n")


# ==============================================================================
# EJEMPLO 3: Buscar producto con bajo stock
# ==============================================================================

def ejemplo_productos_bajo_stock(minimo=5):
    """Encuentra productos con bajo stock"""
    from controllers.producto_controller import ProductoController
    
    resultado = ProductoController.obtener_todos_productos()
    
    if resultado['exito']:
        productos_bajo = [p for p in resultado['datos'] if p.cantidad_stock < minimo]
        
        if productos_bajo:
            print("\\nPRODUCTOS CON BAJO STOCK (< 5):")
            print("-" * 50)
            for p in productos_bajo:
                print(f"{p.codigo}: {p.nombre}")
                print(f"  Stock actual: {p.cantidad_stock}")
                print()
        else:
            print("\\nTodos los productos tienen stock suficiente")


# ==============================================================================
# EJEMPLO 4: Exportar y luego importar
# ==============================================================================

def ejemplo_exportar_importar():
    """Muestra cómo exportar e importar datos"""
    from utils.excel_utils import ExcelUtils
    import datetime
    
    # Exportar productos
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = f"datos_backup_{fecha}.xlsx"
    
    resultado = ExcelUtils.exportar_productos(archivo)
    if resultado['exito']:
        print(f"✓ Datos exportados a {archivo}")
    
    # Importar nuevamente
    resultado = ExcelUtils.importar_productos(archivo)
    if resultado['exito']:
        print(f"✓ {resultado['productos_importados']} productos importados")


# ==============================================================================
# EJEMPLO 5: Estadísticas de productos
# ==============================================================================

def ejemplo_estadisticas():
    """Genera estadísticas sobre productos"""
    from controllers.producto_controller import ProductoController
    from controllers.venta_controller import VentaController
    
    # Obtener productos
    resultado_prod = ProductoController.obtener_todos_productos()
    productos = resultado_prod['datos']
    
    # Obtener ventas
    resultado_vent = VentaController.obtener_todas_ventas()
    ventas = resultado_vent['datos']
    
    # Calcular estadísticas
    total_productos = len(productos)
    total_stock = sum(p.cantidad_stock for p in productos)
    stock_promedio = total_stock / total_productos if total_productos > 0 else 0
    
    valor_inventario = sum(p.precio * p.cantidad_stock for p in productos)
    
    total_ventas = VentaController.obtener_total_ventas()['datos']
    cantidad_ventas = len(ventas)
    
    print("\\n" + "="*50)
    print("ESTADÍSTICAS")
    print("="*50)
    print(f"Total de productos: {total_productos}")
    print(f"Total de stock: {total_stock} unidades")
    print(f"Stock promedio: {stock_promedio:.1f} unidades")
    print(f"Valor del inventario: ${valor_inventario:.2f}")
    print(f"Total de ventas: {cantidad_ventas}")
    print(f"Ingresos totales: ${total_ventas:.2f}")
    if cantidad_ventas > 0:
        print(f"Venta promedio: ${total_ventas/cantidad_ventas:.2f}")
    print("="*50 + "\\n")


# ==============================================================================
# EJEMPLO 6: Actualizar precios en lote
# ==============================================================================

def ejemplo_actualizar_precios(porcentaje_incremento=10):
    """Incrementa los precios de todos los productos"""
    from controllers.producto_controller import ProductoController
    from models.producto import Producto
    
    resultado = ProductoController.obtener_todos_productos()
    
    if resultado['exito']:
        productos = resultado['datos']
        print(f"\\nIncrementando precios en {porcentaje_incremento}%...")
        
        for p in productos:
            nuevo_precio = p.precio * (1 + porcentaje_incremento / 100)
            resultado = ProductoController.actualizar_producto(
                p.id, p.codigo, p.nombre, nuevo_precio, 
                p.cantidad_stock, p.descripcion
            )
            if resultado['exito']:
                print(f"✓ {p.nombre}: ${p.precio:.2f} → ${nuevo_precio:.2f}")


# ==============================================================================
# EJEMPLO 7: Generar lista de compras
# ==============================================================================

def ejemplo_lista_compras_minima(cantidad_minima=10):
    """Genera una lista de qué comprar según el stock mínimo"""
    from controllers.producto_controller import ProductoController
    
    resultado = ProductoController.obtener_todos_productos()
    
    if resultado['exito']:
        productos = resultado['datos']
        productos_comprar = [p for p in productos if p.cantidad_stock < cantidad_minima]
        
        if productos_comprar:
            print("\\nLISTA DE COMPRAS (Stock < 10):")
            print("-" * 50)
            cantidad_total = 0
            for p in productos_comprar:
                cantidad_a_pedir = cantidad_minima - p.cantidad_stock
                costo = cantidad_a_pedir * p.precio
                cantidad_total += costo
                print(f"{p.codigo} - {p.nombre}")
                print(f"  Cantidad a pedir: {cantidad_a_pedir}")
                print(f"  Costo estimado: ${costo:.2f}")
                print()
            print(f"Costo total estimado: ${cantidad_total:.2f}")


# ==============================================================================
# Función main para ejecutar ejemplos
# ==============================================================================

if __name__ == "__main__":
    print("\\n" + "="*60)
    print("EJEMPLOS AVANZADOS DE USO")
    print("="*60)
    
    # Descomenta los ejemplos que quieras ejecutar
    
    # ejemplo_crear_productos_lote()
    # ejemplo_reporte_ventas()
    # ejemplo_productos_bajo_stock()
    # ejemplo_exportar_importar()
    # ejemplo_estadisticas()
    # ejemplo_actualizar_precios(10)
    # ejemplo_lista_compras_minima(10)
    
    print("\\nNota: Descomenta las funciones que desees en el archivo para ejecutar")
