# Gestión de Productos y Ventas

Aplicación de escritorio desarrollada con **Python**, **tkinter** y **SQLite** siguiendo la arquitectura **MVC de N-capas**.

## Características

- ✅ **CRUD completo de productos**
  - Crear, leer, actualizar y eliminar productos
  - Búsqueda y filtrado en tiempo real
  - Gestión de stock

- ✅ **Registro de ventas**
  - Registrar nuevas ventas
  - Editar y eliminar ventas
  - Actualización automática de stock
  - Total de ventas en tiempo real

- ✅ **Importar/Exportar datos**
  - Exportar productos a XLSX
  - Exportar ventas a XLSX
  - Importar productos desde XLSX

- ✅ **Base de datos SQLite**
  - Almacenamiento persistente
  - Integridad referencial
  - Soporta múltiples registros

## Estructura del Proyecto

```
test/
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuración de la aplicación
├── database/
│   ├── __init__.py
│   └── connection.py         # Gestión de conexión a SQLite
├── models/
│   ├── __init__.py
│   ├── producto.py           # Modelo de Productos
│   └── venta.py              # Modelo de Ventas
├── controllers/
│   ├── __init__.py
│   ├── producto_controller.py  # Controlador de Productos
│   └── venta_controller.py     # Controlador de Ventas
├── views/
│   ├── __init__.py
│   ├── main_window.py        # Ventana principal
│   ├── producto_view.py      # Vista de Productos
│   └── venta_view.py         # Vista de Ventas
├── utils/
│   ├── __init__.py
│   └── excel_utils.py        # Utilidades de importar/exportar XLSX
├── data/                      # Carpeta para base de datos (se crea automáticamente)
├── main.py                   # Archivo principal
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

## Requisitos

- Python 3.7+
- tkinter (incluido en Python por defecto)
- openpyxl 3.10.5+

## Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd test
   ```

2. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación:

```bash
python main.py
```

La aplicación abrirá una ventana con la interfaz gráfica lista para usar.

## Uso

### Gestión de Productos

1. **Crear un producto**
   - Click en "Nuevo"
   - Ingresar código, nombre, descripción, precio y cantidad inicial
   - Click en "Guardar"

2. **Editar un producto**
   - Seleccionar el producto en la tabla
   - Click en "Editar"
   - Modificar los datos
   - Click en "Guardar"

3. **Eliminar un producto**
   - Seleccionar el producto en la tabla
   - Click en "Eliminar"
   - Confirmar eliminación

4. **Buscar productos**
   - Escribir en el campo de búsqueda
   - Los resultados se filtran automáticamente

### Gestión de Ventas

1. **Registrar una venta**
   - Click en "Nueva Venta"
   - Seleccionar el producto
   - Ingresar cantidad y precio unitario
   - Click en "Guardar"

2. **Editar una venta**
   - Seleccionar la venta en la tabla
   - Click en "Editar"
   - Modificar cantidad o precio
   - Click en "Guardar"

3. **Eliminar una venta**
   - Seleccionar la venta en la tabla
   - Click en "Eliminar"
   - Confirmar eliminación

4. **Ver total de ventas**
   - El total se muestra en tiempo real en la parte superior

### Importar/Exportar

1. **Exportar productos**
   - Click en "Exportar Productos"
   - Seleccionar ubicación y nombre del archivo
   - El archivo XLSX se crea automáticamente

2. **Exportar ventas**
   - Click en "Exportar Ventas"
   - Seleccionar ubicación y nombre del archivo
   - Incluye subtotales y total general

3. **Importar productos**
   - Click en "Importar Productos"
   - Seleccionar archivo XLSX con productos
   - La aplicación importa los datos válidos

## Formato de Importación

### Para productos (XLSX):
| ID | Código | Nombre | Descripción | Precio | Stock |
|----|--------|--------|-------------|--------|-------|
| - | PROD001 | Producto 1 | Descripción | 100.00 | 50 |
| - | PROD002 | Producto 2 | Descripción | 200.00 | 30 |

Nota: El ID se genera automáticamente

## Base de Datos

La aplicación usa SQLite con las siguientes tablas:

### Tabla: productos
- `id`: Identificador único (autoincremento)
- `codigo`: Código único del producto
- `nombre`: Nombre del producto
- `descripcion`: Descripción del producto
- `precio`: Precio unitario
- `cantidad_stock`: Cantidad disponible en stock
- `fecha_creacion`: Timestamp de creación
- `fecha_actualizacion`: Timestamp de última actualización

### Tabla: ventas
- `id`: Identificador único (autoincremento)
- `producto_id`: Referencia al producto vendido
- `cantidad`: Cantidad vendida
- `precio_unitario`: Precio al momento de la venta
- `subtotal`: Total de la venta (cantidad × precio)
- `fecha_venta`: Timestamp de la venta

## Características Técnicas

### Arquitectura MVC
- **Models**: Lógica de datos (producto.py, venta.py)
- **Controllers**: Lógica de negocio (producto_controller.py, venta_controller.py)
- **Views**: Interfaz gráfica (producto_view.py, venta_view.py)

### N-Capas
- **Capa de Presentación**: views/
- **Capa de Controladores**: controllers/
- **Capa de Modelos/Datos**: models/
- **Capa de Acceso a Datos**: database/
- **Capa de Utilidades**: utils/

### Validaciones
- Validación de datos de entrada
- Verificación de stock disponible
- Integridad referencial en base de datos
- Mensajes de error descriptivos

## Notas Importantes

- El archivo de base de datos se crea automáticamente en `data/app.db`
- El stock se reduce automáticamente al registrar una venta
- Al eliminar una venta, el stock se restaura
- Los códigos de productos deben ser únicos
- Se pueden exportar/importar múltiples registros

## Autor

Aplicación de gestión de productos y ventas - 2026

## Licencia

MIT