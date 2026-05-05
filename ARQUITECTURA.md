# Arquitectura de la Aplicación

## Patrón MVC de N-Capas

Esta aplicación implementa una arquitectura MVC (Model-View-Controller) de múltiples capas para asegurar separación de responsabilidades y facilitar el mantenimiento.

```
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE PRESENTACIÓN (UI)                 │
│                     (views/*.py)                             │
│  ┌──────────────────┬──────────────────┬──────────────────┐  │
│  │ main_window.py   │ producto_view.py │  venta_view.py   │  │
│  │ (Interfaz)       │ (Productos)      │  (Ventas)        │  │
│  └──────────────────┴──────────────────┴──────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              CAPA DE CONTROLADORES                           │
│            (controllers/*.py)                                │
│  ┌──────────────────────────┬──────────────────────────┐    │
│  │ ProductoController       │ VentaController          │    │
│  │ - crear_producto()       │ - crear_venta()          │    │
│  │ - obtener_todos()        │ - obtener_todas()        │    │
│  │ - actualizar_producto()  │ - actualizar_venta()     │    │
│  │ - eliminar_producto()    │ - eliminar_venta()       │    │
│  └──────────────────────────┴──────────────────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              CAPA DE MODELOS/DATOS                           │
│                (models/*.py)                                 │
│  ┌──────────────────────────┬──────────────────────────┐    │
│  │ Producto                 │ Venta                    │    │
│  │ - crear()                │ - crear()                │    │
│  │ - obtener_todos()        │ - obtener_todas()        │    │
│  │ - obtener_por_id()       │ - obtener_por_id()       │    │
│  │ - actualizar()           │ - actualizar()           │    │
│  │ - eliminar()             │ - eliminar()             │    │
│  │ - obtener_por_codigo()   │ - obtener_total_ventas() │    │
│  └──────────────────────────┴──────────────────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         CAPA DE ACCESO A DATOS (DATABASE)                    │
│              (database/*.py)                                 │
│  ┌───────────────────────────────────────────────────┐      │
│  │ DatabaseConnection                               │      │
│  │ - get_connection()                                │      │
│  │ - close_connection()                              │      │
│  │ - create_tables()                                 │      │
│  └───────────────────────────────────────────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│               SQLite Database                                │
│  ┌──────────────────┬──────────────────┐                     │
│  │    productos     │     ventas       │                     │
│  │  id (PK)         │  id (PK)         │                     │
│  │  codigo (UNIQUE) │  producto_id (FK)│                     │
│  │  nombre          │  cantidad        │                     │
│  │  descripcion     │  precio_unitario │                     │
│  │  precio          │  subtotal        │                     │
│  │  cantidad_stock  │  fecha_venta     │                     │
│  │  timestamps      │                  │                     │
│  └──────────────────┴──────────────────┘                     │
└────────────────────────────────────────────────────────────┘
```

## Capas y Responsabilidades

### 1. Capa de Presentación (Views)
**Ubicación:** `views/`

Responsable de la interfaz gráfica usando tkinter.

- **main_window.py**: Ventana principal con pestañas
- **producto_view.py**: Interfaz para gestión de productos
- **venta_view.py**: Interfaz para gestión de ventas

**Responsabilidades:**
- Mostrar datos en la UI
- Capturar eventos del usuario
- Validación básica de campos
- Mostrar mensajes al usuario

### 2. Capa de Controladores (Controllers)
**Ubicación:** `controllers/`

Lógica de negocio de la aplicación.

- **producto_controller.py**: Operaciones CRUD de productos
- **venta_controller.py**: Operaciones CRUD de ventas

**Responsabilidades:**
- Validar datos de entrada
- Ejecutar reglas de negocio
- Coordinar entre vistas y modelos
- Manejo de excepciones
- Retornar resultados estructurados

### 3. Capa de Modelos (Models)
**Ubicación:** `models/`

Interacción con la base de datos.

- **producto.py**: Modelo de Producto
- **venta.py**: Modelo de Venta

**Responsabilidades:**
- Consultas SQL
- Gestión de datos
- Mapeo de datos del BD a objetos Python
- Operaciones CRUD a nivel de BD

### 4. Capa de Acceso a Datos (Database)
**Ubicación:** `database/`

Gestión de la conexión a la base de datos.

- **connection.py**: Singleton para conexión SQLite

**Responsabilidades:**
- Conexión a SQLite
- Creación de tablas
- Pool de conexiones (simple)

### 5. Capas de Utilidades
**Ubicación:** `config/` y `utils/`

- **config/settings.py**: Configuraciones globales
- **utils/excel_utils.py**: Importar/exportar XLSX

## Flujo de Datos

### Ejemplo: Crear un producto

```
Usuario
   ↓
[Vista] ProductoView.nueva_ventana_crear()
   ↓
[Usuario ingresa datos y hace click en Guardar]
   ↓
[Controlador] ProductoController.crear_producto()
✓ Valida datos
   ↓
[Modelo] Producto.crear()
   ↓
[Base de Datos] INSERT INTO productos
   ↓
[Retorno] {"exito": True, "id": 1}
   ↓
[Vista] Actualiza tabla y muestra mensaje
```

### Ejemplo: Registrar una venta

```
Usuario
   ↓
[Vista] VentaView.nueva_ventana_crear()
   ↓
[Usuario selecciona producto, cantidad y precio]
   ↓
[Controlador] VentaController.crear_venta()
✓ Valida cantidad y precio
✓ Verifica stock disponible
✓ Obtiene producto
   ↓
[Modelo] Venta.crear()
   ↓
[Base de Datos] INSERT INTO ventas
   ↓
[Controlador] Actualiza stock del producto
   ↓
[Modelo] Producto.actualizar()
   ↓
[Base de Datos] UPDATE productos
   ↓
[Vista] Actualiza tabla de ventas
```

## Ventajas de esta Arquitectura

1. **Separación de Responsabilidades**
   - Cada capa tiene una responsabilidad única y bien definida

2. **Mantenibilidad**
   - Es fácil encontrar y modificar código
   - Cambios en una capa no afectan directamente a otras

3. **Testabilidad**
   - Cada componente se puede probar de forma aislada

4. **Escalabilidad**
   - Fácil agregar nuevas funcionalidades
   - Se puede migrar la UI fácilmente

5. **Reutilización**
   - Los controladores pueden ser usados por otras interfaces (CLI, API web, etc.)

## Dependencias entre Capas

```
Presentación  → Controladores
                      ↓
                  Modelos → Base de Datos
                      ↓
                  Utilidades
```

- Las vistas no acceden directamente a la BD
- Los modelos no conocen sobre la UI
- Los controladores coordinan la lógica

## Ejemplo de Agregar Nueva Funcionalidad

Si queremos agregar una "Capa de Reportes":

1. **Crear modelo**: `models/reporte.py`
   - Lógica de consultas para reportes

2. **Crear controlador**: `controllers/reporte_controller.py`
   - Lógica de negocio para reportes

3. **Crear vista**: `views/reporte_view.py`
   - Interfaz gráfica de reportes

4. **Agregar a main_window.py**: Nueva pestaña

Sin modificar el código existente de productos o ventas.

## Buenas Prácticas Seguidas

✓ DRY (Don't Repeat Yourself)
✓ SOLID Principles
✓ Single Responsibility Principle
✓ Separación de Responsabilidades
✓ Código documentado y legible
✓ Manejo consistente de errores
