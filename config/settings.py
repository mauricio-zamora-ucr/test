# Configuración de la aplicación
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'app.db')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Crear directorio data si no existe
os.makedirs(DATA_DIR, exist_ok=True)

# Configuración de la ventana principal
WINDOW_TITLE = "Gestión de Productos y Ventas"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"

# Configuración de estilos
FONT_TITLE = ("Arial", 14, "bold")
FONT_LABEL = ("Arial", 10)
FONT_BUTTON = ("Arial", 10)
