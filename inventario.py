import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class Inventario(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn =  sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()
        
    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase, ruta)
    
    def widgets(self):
        frame1 = tk.Frame(self, bg="#959595", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x= 0, y= 0, width= 1100, height= 100)
        
        #Titulo
        titulo = tk.Label(self, text= "INVENTARIO", bg="#959595", font=("rockwell 30"), anchor="center")
        titulo.pack()
        titulo.place(x= 5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#dddddd", highlightbackground="black", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        #Productos
        labelframe = LabelFrame(frame2, text="Productos:", font=("rockwell", 18), bg="#dddddd")
        labelframe.place(x=20, y=30, width=400, height=500)
        
        #Label nombre
        lblnombre = Label(labelframe, text="Nombre: ", font=("rockwell", 12), bg="#dddddd")
        lblnombre.place(x=10, y=30)
        self.nombre = ttk.Entry(labelframe, font=("rockwell", 12))
        self.nombre.place(x=140, y=20, width=240, height=40)
        
        #Label proveedor
        lblproveedor = Label(labelframe, text="Proveedor:", font=("rockwell", 12), bg="#dddddd")
        lblproveedor.place(x=10, y=90)
        self.proveedor = ttk.Entry(labelframe, font=("rockwell", 12))
        self.proveedor.place(x=140, y=80, width=240, height=40)
        
        #Label precio
        lblprecio = Label(labelframe, text="Precio:", font=("rockwell", 12), bg="#dddddd")
        lblprecio.place(x=10, y=150)
        self.precio = ttk.Entry(labelframe, font=("rockwell", 12))
        self.precio.place(x=140, y=140, width=240, height=40)
        
        #Label costo
        lblcosto = Label(labelframe, text="Costo:", font=("rockwell", 12), bg="#dddddd")
        lblcosto.place(x=10, y=210)
        self.costo = ttk.Entry(labelframe, font=("rockwell", 12))
        self.costo.place(x=140, y=200, width=240, height=40)
        
        #Label stock
        lblstock = Label(labelframe, text="Stock:", font=("rockwell", 12), bg="#dddddd")
        lblstock.place(x=10, y=270)
        self.stock = ttk.Entry(labelframe, font=("rockwell", 12))
        self.stock.place(x=140, y=260, width=240, height=40)
        
        #Boton agregar
        boton_agregar = tk.Button(labelframe, text="Ingresar", font=("rockwell", 12), bg="#959595", command=self.registrar)
        boton_agregar.place(x=80, y=340, width=240, height=40)
        
        #Boton editar
        boton_editar = tk.Button(labelframe, text="Editar", font=("rockwell", 12), bg="#959595", command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=40)
        
        #Tabla
        treFrame = Frame(frame2, bg="white")
        treFrame.place(x=450, y=50, width=620, height=400)
        
        scroll_y = ttk.Scrollbar(treFrame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=40,
                                columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "COSTO", "STOCK"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scroll_y.config(command=self.tre.yview)
        scroll_x.config(command=self.tre.xview)
        
        self.tre.heading("ID", text="Id")
        self.tre.heading("PRODUCTO", text="Producto")
        self.tre.heading("PROVEEDOR", text="Proveedor")
        self.tre.heading("PRECIO", text="Precio")
        self.tre.heading("COSTO", text="Costo")
        self.tre.heading("STOCK", text="Stock")
        
        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("PRODUCTO", width=150, anchor="center")
        self.tre.column("PROVEEDOR", width=100, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("STOCK", width=50, anchor="center")
        
        self.mostrar()
        
        #Boton actualizar
        btn_actualizar = Button(frame2, text="Actualizar", bg="#959595", font=("rockwell", 12), command=self.actualizar_inventario)
        btn_actualizar.place(x=480, y=480, width=260, height=50)
        
        #Boton eliminar
        btn_eliminar =  Button(frame2, text="Eliminar", bg="#959595", font=("rockwell", 12), command=self.eliminar_producto)
        btn_eliminar.place(x=780, y=480, width=260, height=50)
        
    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result
    
    def validacion(self, nombre, proveedor, precio, costo, stock):
        if not nombre and proveedor and precio and costo and stock:
            return False
        try:
            float(precio)
            float(costo)
            int(costo)
        except ValueError:
            return False
        return True
    
    def mostrar(self):
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result:
            try:
                precio_mil = "{:,.0f} $".format(float(elem[3])) if elem[3] else ""
                costo_mil = "{:,.0f} $".format(float(elem[4])) if elem[4] else ""
            except ValueError:
                precio_mil = elem[3]
                costo_mil = elem[4]
            self.tre.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio_mil, costo_mil, elem[5]))
            
    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.mostrar()
        messagebox.showinfo("Actualizacion", "El inventario ha sido actualizado")
    
    def eliminar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning(title="Eliminar producto", message="Seleccione un producto para eliminar")
            return
        item_id = self.tre.item(seleccion)["text"]

        # Confirmar la eliminación
        confirmar = messagebox.askyesno(title="Confirmar eliminación",
                                    message=f"¿Está seguro que desea eliminar el producto con ID {item_id}?")
        if confirmar:
            try:
                consulta = "DELETE FROM inventario WHERE id=?"
                parametros = (item_id,)
                self.eje_consulta(consulta, parametros)
                self.actualizar_inventario()
                messagebox.showinfo("Eliminación exitosa", "El producto ha sido eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el producto: {e}")
        
        
    def registrar(self):
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        nombre = self.nombre.get()
        proveedor = self.proveedor.get()
        precio =  self.precio.get()
        costo =  self.costo.get()
        stock =  self.stock.get()
        if self.validacion(nombre, proveedor, precio, costo, stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?, ?, ?, ?, ?, ?)"
                parametros = (None, nombre, proveedor, precio, costo, stock)
                self.eje_consulta(consulta, parametros)
                self.mostrar()
                self.nombre.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
            except Exception as e:
                messagebox.showwarning(title="Error", message=f"Error al registrar el producto: {e}")
        else: 
            messagebox.showwarning(title="Error", message="Rellene todos los campos correctamente")
            self.mostrar()
    
    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning(title="Editar producto", message="Seleccione un producto para editar")
            return 
        
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]
        
        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#dddddd")
        
        lbl_nombre = Label(ventana_editar, text="Nombre:", font=("rockwell", 12), bg="#dddddd")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font=("rockwell", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])
        
        lbl_proveedor = Label(ventana_editar, text="Proveedor:", font=("rockwell", 12), bg="#dddddd")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font=("rockwell", 12))
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])
        
        lbl_precio = Label(ventana_editar, text="Precio:", font=("rockwell", 12), bg="#dddddd")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font=("rockwell", 12))
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].split()[0].replace(",", ""))
        
        lbl_costo = Label(ventana_editar, text="Costo:", font=("rockwell", 12), bg="#dddddd")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font=("rockwell", 12))
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].split()[0].replace(",", ""))
        
        lbl_stock = Label(ventana_editar, text="Stock:", font=("rockwell", 12), bg="#dddddd")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font=("rockwell", 12))
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])
        
        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo =  entry_costo.get()
            stock = entry_stock.get()
            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos")
                return
            try:
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showwarning("Guardar cambios", "Ingrese valores numericos validos para precio y costo")
                return
            
            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)
            self.actualizar_inventario()
            ventana_editar.destroy()
        
        btn_guardar = Button(ventana_editar, text="Guardar cambios", bg="#959595", font=("rockwell", 12), command=guardar_cambios)
        btn_guardar.place(x=80, y=310, width=240, height=40)