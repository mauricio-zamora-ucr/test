"""
Vista principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from views.producto_view import ProductoView
from views.venta_view import VentaView


class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos y Ventas")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Crear frame superior para el título
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text="Gestión de Productos y Ventas",
            font=("Arial", 16, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab de Productos
        producto_frame = ttk.Frame(self.notebook)
        self.notebook.add(producto_frame, text="Productos")
        self.producto_view = ProductoView(producto_frame, self.root)
        
        # Tab de Ventas
        venta_frame = ttk.Frame(self.notebook)
        self.notebook.add(venta_frame, text="Ventas")
        self.venta_view = VentaView(venta_frame, self.root)
        
        # Frame inferior con botones
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            footer_frame,
            text="Exportar Productos",
            command=self.exportar_productos
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            footer_frame,
            text="Exportar Ventas",
            command=self.exportar_ventas
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            footer_frame,
            text="Importar Productos",
            command=self.importar_productos
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            footer_frame,
            text="Salir",
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=5)
    
    def exportar_productos(self):
        """Exporta los productos a un archivo XLSX"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"productos_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if ruta:
            from utils.excel_utils import ExcelUtils
            resultado = ExcelUtils.exportar_productos(ruta)
            if resultado['exito']:
                messagebox.showinfo("Éxito", resultado['mensaje'])
            else:
                messagebox.showerror("Error", resultado['mensaje'])
    
    def exportar_ventas(self):
        """Exporta las ventas a un archivo XLSX"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"ventas_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if ruta:
            from utils.excel_utils import ExcelUtils
            resultado = ExcelUtils.exportar_ventas(ruta)
            if resultado['exito']:
                messagebox.showinfo("Éxito", resultado['mensaje'])
            else:
                messagebox.showerror("Error", resultado['mensaje'])
    
    def importar_productos(self):
        """Importa productos desde un archivo XLSX"""
        ruta = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if ruta:
            from utils.excel_utils import ExcelUtils
            resultado = ExcelUtils.importar_productos(ruta)
            if resultado['exito']:
                mensaje = resultado['mensaje']
                if resultado['errores']:
                    mensaje += "\n\nErrores:\n" + "\n".join(resultado['errores'][:5])
                    if len(resultado['errores']) > 5:
                        mensaje += f"\n... y {len(resultado['errores']) - 5} errores más"
                messagebox.showinfo("Importación", mensaje)
                self.producto_view.actualizar_tabla()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
