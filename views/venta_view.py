"""
Vista para gestionar ventas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.venta_controller import VentaController
from controllers.producto_controller import ProductoController


class VentaView:
    """Vista para operaciones CRUD de ventas"""
    
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.venta_seleccionada = None
        
        self.setup_ui()
        self.actualizar_tabla()
        self.actualizar_productos()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame superior para controles
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Frame para botones
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Nueva Venta",
            command=self.nueva_ventana_crear
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="Editar",
            command=self.nueva_ventana_editar
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="Eliminar",
            command=self.eliminar_venta
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="Actualizar",
            command=self.actualizar_tabla
        ).pack(side=tk.LEFT, padx=2)
        
        # Frame para el total
        total_frame = ttk.LabelFrame(top_frame, text="Total de Ventas", padding=5)
        total_frame.pack(side=tk.LEFT, padx=5)
        self.total_label = ttk.Label(total_frame, text="$0.00", font=("Arial", 12, "bold"))
        self.total_label.pack()
        
        # Frame para la tabla
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Cod. Producto", "Nombre", "Cantidad", "Precio Unit.", "Subtotal", "Fecha"),
            height=20,
            show="headings"
        )
        
        # Configurar columnas
        self.tree.column("ID", width=40)
        self.tree.column("Cod. Producto", width=80)
        self.tree.column("Nombre", width=150)
        self.tree.column("Cantidad", width=80)
        self.tree.column("Precio Unit.", width=100)
        self.tree.column("Subtotal", width=100)
        self.tree.column("Fecha", width=150)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cod. Producto", text="Cod. Producto")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio Unit.", text="Precio Unit.")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.heading("Fecha", text="Fecha")
        
        # Asociar evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_fila)
        
        # Scrollbar vertical
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        
        # Scrollbar horizontal
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def actualizar_tabla(self):
        """Actualiza los datos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener ventas
        resultado = VentaController.obtener_todas_ventas()
        if resultado['exito']:
            for venta in resultado['datos']:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        venta['id'],
                        venta['codigo_producto'],
                        venta['nombre_producto'],
                        venta['cantidad'],
                        f"${venta['precio_unitario']:.2f}",
                        f"${venta['subtotal']:.2f}",
                        venta['fecha_venta']
                    ),
                    tags=(venta['id'],)
                )
        
        # Actualizar total
        resultado_total = VentaController.obtener_total_ventas()
        if resultado_total['exito']:
            total = resultado_total['datos']
            self.total_label.config(text=f"${total:.2f}")
    
    def seleccionar_fila(self, event):
        """Maneja la selección de una fila"""
        selección = self.tree.selection()
        if selección:
            item = selección[0]
            self.venta_seleccionada = self.tree.item(item)['tags'][0]
    
    def actualizar_productos(self):
        """Actualiza la lista de productos disponibles"""
        resultado = ProductoController.obtener_todos_productos()
        self.productos = []
        if resultado['exito']:
            for p in resultado['datos']:
                self.productos.append({
                    'id': p.id,
                    'codigo': p.codigo,
                    'nombre': p.nombre,
                    'precio': p.precio,
                    'stock': p.cantidad_stock
                })
    
    def nueva_ventana_crear(self):
        """Abre ventana para crear una nueva venta"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nueva Venta")
        ventana.geometry("500x250")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Actualizar productos
        self.actualizar_productos()
        
        # Crear campos
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Producto:").grid(row=0, column=0, sticky=tk.W, pady=10)
        productos_nombres = [f"{p['codigo']} - {p['nombre']}" for p in self.productos]
        producto_combo = ttk.Combobox(frame, values=productos_nombres, state="readonly", width=40)
        producto_combo.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=10)
        cantidad_entry = ttk.Entry(frame, width=40)
        cantidad_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Precio Unitario:").grid(row=2, column=0, sticky=tk.W, pady=10)
        precio_entry = ttk.Entry(frame, width=40)
        precio_entry.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def guardar():
            try:
                indice = producto_combo.current()
                if indice < 0:
                    messagebox.showwarning("Atención", "Selecciona un producto")
                    return
                
                producto = self.productos[indice]
                cantidad = int(cantidad_entry.get())
                precio = float(precio_entry.get())
                
                resultado = VentaController.crear_venta(producto['id'], cantidad, precio)
                
                if resultado['exito']:
                    messagebox.showinfo("Éxito", resultado['mensaje'])
                    self.actualizar_tabla()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", resultado['mensaje'])
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        
        def actualizar_precio(*args):
            indice = producto_combo.current()
            if indice >= 0:
                precio_entry.delete(0, tk.END)
                precio_entry.insert(0, str(self.productos[indice]['precio']))
        
        producto_combo.bind('<<ComboboxSelected>>', actualizar_precio)
        
        ttk.Button(button_frame, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=ventana.destroy).pack(side=tk.LEFT, padx=5)
    
    def nueva_ventana_editar(self):
        """Abre ventana para editar la venta seleccionada"""
        if not self.venta_seleccionada:
            messagebox.showwarning("Atención", "Selecciona una venta para editar")
            return
        
        resultado = VentaController.obtener_venta(self.venta_seleccionada)
        if not resultado['exito']:
            messagebox.showerror("Error", resultado['mensaje'])
            return
        
        venta = resultado['datos']
        
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Editar Venta - {venta['nombre_producto']}")
        ventana.geometry("500x250")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Crear campos
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Producto:").grid(row=0, column=0, sticky=tk.W, pady=10)
        producto_label = ttk.Label(frame, text=f"{venta['codigo_producto']} - {venta['nombre_producto']}")
        producto_label.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=10)
        cantidad_entry = ttk.Entry(frame, width=40)
        cantidad_entry.insert(0, str(venta['cantidad']))
        cantidad_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Precio Unitario:").grid(row=2, column=0, sticky=tk.W, pady=10)
        precio_entry = ttk.Entry(frame, width=40)
        precio_entry.insert(0, str(venta['precio_unitario']))
        precio_entry.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def guardar():
            try:
                cantidad = int(cantidad_entry.get())
                precio = float(precio_entry.get())
                
                resultado = VentaController.actualizar_venta(
                    self.venta_seleccionada, cantidad, precio
                )
                
                if resultado['exito']:
                    messagebox.showinfo("Éxito", resultado['mensaje'])
                    self.actualizar_tabla()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", resultado['mensaje'])
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        
        ttk.Button(button_frame, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=ventana.destroy).pack(side=tk.LEFT, padx=5)
    
    def eliminar_venta(self):
        """Elimina la venta seleccionada"""
        if not self.venta_seleccionada:
            messagebox.showwarning("Atención", "Selecciona una venta para eliminar")
            return
        
        if messagebox.askyesno("Confirmación", "¿Deseas eliminar esta venta?"):
            resultado = VentaController.eliminar_venta(self.venta_seleccionada)
            
            if resultado['exito']:
                messagebox.showinfo("Éxito", resultado['mensaje'])
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
