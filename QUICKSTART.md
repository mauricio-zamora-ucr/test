# Guía de Inicio Rápido

## 1. Instalación (5 minutos)

```bash
cd /ruta/del/proyecto
pip install -r requirements.txt
```

## 2. Crear datos de ejemplo (Opcional)

Para cargar datos de demostración:

```bash
python demo.py
```

Esto creará:
- 6 productos de ejemplo
- 5 ventas de ejemplo

## 3. Ejecutar la aplicación

```bash
python main.py
```

La ventana principal se abrirá automáticamente.

## Primer uso

### Opción A: Comenzar vacío
1. Click en "Nuevo" en la pestaña "Productos"
2. Ingresa los datos del producto
3. Click en "Guardar"

### Opción B: Importar datos
1. Click en "Importar Productos"
2. Selecciona un archivo XLSX con productos
3. Los datos se importarán automáticamente

## Tareas comunes

### Registrar una venta
1. Ve a la pestaña "Ventas"
2. Click en "Nueva Venta"
3. Selecciona un producto
4. Ingresa cantidad y precio
5. Click en "Guardar"

**Nota:** El stock se actualiza automáticamente

### Exportar datos
1. Click en "Exportar Productos" o "Exportar Ventas"
2. Elige dónde guardar el archivo
3. El archivo XLSX se genera automáticamente

### Buscar productos
1. En la pestaña "Productos"
2. Escribe en el campo de búsqueda
3. Los resultados se filtran en tiempo real

## Estructura de base de datos

La aplicación crea automáticamente:
- Base de datos: `/data/app.db`
- Tablas: `productos` y `ventas`

No necesitas hacer nada, todo se genera automáticamente.

## Solución de problemas

### "ModuleNotFoundError: No module named 'openpyxl'"
```bash
pip install -r requirements.txt
```

### La aplicación no inicia
Verifica que tienes Python 3.7+ instalado:
```bash
python --version
```

### Error al importar archivos XLSX
Asegúrate de que el archivo tiene el formato correcto:
- Las columnas deben ser: Código, Nombre, Descripción, Precio, Stock
- Los precios deben ser números
- Los códigos deben ser únicos

## Ejemplos de uso

### Crear productos programáticamente

```python
from controllers.producto_controller import ProductoController

resultado = ProductoController.crear_producto(
    codigo="PROD001",
    nombre="Mi Producto",
    precio=99.99,
    cantidad_stock=10,
    descripcion="Descripción del producto"
)

if resultado['exito']:
    print(f"Producto creado con ID: {resultado['id']}")
```

### Registrar una venta programáticamente

```python
from controllers.venta_controller import VentaController

resultado = VentaController.crear_venta(
    producto_id=1,
    cantidad=5,
    precio_unitario=99.99
)

if resultado['exito']:
    print(f"Venta registrada con ID: {resultado['id']}")
```

## ¿Necesitas ayuda?

- Lee el archivo README.md para documentación completa
- Revisa el código - está bien documentado
- Crea un issue en GitHub si encuentras un problema

¡Que disfrutes usando la aplicación!
