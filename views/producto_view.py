"""
Vista para gestionar productos
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.producto_controller import ProductoController


class ProductoView:
    """Vista para operaciones CRUD de productos"""
    
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.producto_seleccionado = None
        
        self.setup_ui()
        self.actualizar_tabla()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame superior para búsqueda y controles
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filtrar_tabla)
        
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Frame para botones
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Nuevo",
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
            command=self.eliminar_producto
        ).pack(side=tk.LEFT, padx=2)
        
        # Frame para la tabla
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Código", "Nombre", "Descripción", "Precio", "Stock"),
            height=20,
            show="headings"
        )
        
        # Configurar columnas
        self.tree.column("ID", width=40)
        self.tree.column("Código", width=80)
        self.tree.column("Nombre", width=150)
        self.tree.column("Descripción", width=200)
        self.tree.column("Precio", width=80)
        self.tree.column("Stock", width=80)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        
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
        
        # Obtener productos
        resultado = ProductoController.obtener_todos_productos()
        if resultado['exito']:
            for producto in resultado['datos']:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        producto.id,
                        producto.codigo,
                        producto.nombre,
                        producto.descripcion,
                        f"${producto.precio:.2f}",
                        producto.cantidad_stock
                    ),
                    tags=(producto.id,)
                )
    
    def filtrar_tabla(self, *args):
        """Filtra la tabla según el texto de búsqueda"""
        search_text = self.search_var.get().lower()
        
        resultado = ProductoController.obtener_todos_productos()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Mostrar solo los elementos que coinciden
        if resultado['exito']:
            for producto in resultado['datos']:
                if (search_text in producto.codigo.lower() or
                    search_text in producto.nombre.lower() or
                    search_text in producto.descripcion.lower()):
                    self.tree.insert(
                        "",
                        tk.END,
                        values=(
                            producto.id,
                            producto.codigo,
                            producto.nombre,
                            producto.descripcion,
                            f"${producto.precio:.2f}",
                            producto.cantidad_stock
                        ),
                        tags=(producto.id,)
                    )
    
    def seleccionar_fila(self, event):
        """Maneja la selección de una fila"""
        selección = self.tree.selection()
        if selección:
            item = selección[0]
            self.producto_seleccionado = self.tree.item(item)['tags'][0]
    
    def nueva_ventana_crear(self):
        """Abre ventana para crear un nuevo producto"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Producto")
        ventana.geometry("500x400")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Crear campos
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Código:").grid(row=0, column=0, sticky=tk.W, pady=10)
        codigo_entry = ttk.Entry(frame, width=30)
        codigo_entry.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=10)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky=tk.W+tk.N, pady=10)
        descripcion_text = tk.Text(frame, width=30, height=5)
        descripcion_text.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Precio:").grid(row=3, column=0, sticky=tk.W, pady=10)
        precio_entry = ttk.Entry(frame, width=30)
        precio_entry.grid(row=3, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Cantidad Stock:").grid(row=4, column=0, sticky=tk.W, pady=10)
        stock_entry = ttk.Entry(frame, width=30)
        stock_entry.grid(row=4, column=1, sticky=tk.W, pady=10)
        
        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def guardar():
            try:
                codigo = codigo_entry.get()
                nombre = nombre_entry.get()
                descripcion = descripcion_text.get("1.0", tk.END).strip()
                precio = float(precio_entry.get())
                cantidad = int(stock_entry.get())
                
                resultado = ProductoController.crear_producto(
                    codigo, nombre, precio, cantidad, descripcion
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
    
    def nueva_ventana_editar(self):
        """Abre ventana para editar el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para editar")
            return
        
        resultado = ProductoController.obtener_producto(self.producto_seleccionado)
        if not resultado['exito']:
            messagebox.showerror("Error", resultado['mensaje'])
            return
        
        producto = resultado['datos']
        
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Editar Producto - {producto.nombre}")
        ventana.geometry("500x400")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Crear campos
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Código:").grid(row=0, column=0, sticky=tk.W, pady=10)
        codigo_entry = ttk.Entry(frame, width=30)
        codigo_entry.insert(0, producto.codigo)
        codigo_entry.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=10)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.insert(0, producto.nombre)
        nombre_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky=tk.W+tk.N, pady=10)
        descripcion_text = tk.Text(frame, width=30, height=5)
        descripcion_text.insert("1.0", producto.descripcion)
        descripcion_text.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Precio:").grid(row=3, column=0, sticky=tk.W, pady=10)
        precio_entry = ttk.Entry(frame, width=30)
        precio_entry.insert(0, str(producto.precio))
        precio_entry.grid(row=3, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(frame, text="Cantidad Stock:").grid(row=4, column=0, sticky=tk.W, pady=10)
        stock_entry = ttk.Entry(frame, width=30)
        stock_entry.insert(0, str(producto.cantidad_stock))
        stock_entry.grid(row=4, column=1, sticky=tk.W, pady=10)
        
        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def guardar():
            try:
                codigo = codigo_entry.get()
                nombre = nombre_entry.get()
                descripcion = descripcion_text.get("1.0", tk.END).strip()
                precio = float(precio_entry.get())
                cantidad = int(stock_entry.get())
                
                resultado = ProductoController.actualizar_producto(
                    self.producto_seleccionado, codigo, nombre, precio, cantidad, descripcion
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
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmación", "¿Deseas eliminar este producto?"):
            resultado = ProductoController.eliminar_producto(self.producto_seleccionado)
            
            if resultado['exito']:
                messagebox.showinfo("Éxito", resultado['mensaje'])
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
