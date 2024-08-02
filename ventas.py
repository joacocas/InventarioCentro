import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class Ventas(tk.Frame):
    db_name = "database.db"
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.widgets()
        
    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase, ruta)
        
    def widgets(self):
        frame1 = tk.Frame(self, bg="#959595", highlightbackground="gray", highlightthickness=1)
        frame1.place(x=0, y=0, width=1100, height=100)
        
        titulo = tk.Label(self, text="VENTAS", bg="#959595", font=("rockwell", 30), anchor="center")
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#dddddd", highlightbackground="black", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        lblframe = tk.LabelFrame(frame2, text="Información de la venta", bg="#dddddd", font=("rockwell", 18))
        lblframe.place(x=10, y=10, width=1060, height=80)
        
        # Label nombre de producto
        label_nombre = tk.Label(lblframe, text="Producto:", bg="#dddddd", font=("rockwell", 12))
        label_nombre.place(x=50, y=10)
        self.entry_nombre = ttk.Combobox(lblframe, font=("rockwell", 12), state="readonly")
        self.entry_nombre.place(x=130, y=7, width=180, height=32)
        
        self.cargar_productos()
        
        # Label precio
        label_valor = tk.Label(lblframe, text="Precio:", bg="#dddddd", font=("rockwell", 12))
        label_valor.place(x=380, y=10)
        self.entry_valor = ttk.Entry(lblframe, font=("rockwell", 12), state="readonly")
        self.entry_valor.place(x=440, y=7, width=180)
        
        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio)
        
        # Label cantidad
        label_cantidad = tk.Label(lblframe, text="Cantidad:", bg="#dddddd", font=("rockwell", 12))
        label_cantidad.place(x=690, y=10)
        self.entry_cantidad = ttk.Entry(lblframe, font=("rockwell", 12))
        self.entry_cantidad.place(x=770, y=7, width=180)
        
        treFrame = tk.Frame(frame2,  bg="#dddddd")
        treFrame.place(x=100, y=120, width=900, height=260)
        
        scroll_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tree = ttk.Treeview(treFrame, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=20, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")
        
        self.tree.column("Producto", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")
        
        self.tree.pack(expand=True, fill=BOTH)
        
        lblframe1 = LabelFrame(frame2, text="Opciones", bg="#dddddd", font=("rockwell", 12))
        lblframe1.place(x=10, y=440, width=1060, height=100)
        
        #Boton agregar
        boton_agregar = tk.Button(lblframe1, text="Agregar", bg="#959595", font=("rockwell", 12), command=self.registrar)
        boton_agregar.place(x=80, y=10, width=400, height=50)
        
        #Boton pagar
        boton_pagar = tk.Button(lblframe1, text="Pagar", bg="#959595", font=("rockwell", 12), command=self.abrir_ventana_pago)
        boton_pagar.place(x=580, y=10, width=400, height=50)
        
        self.label_suma_total = tk.Label(frame2, text="Total a pagar: $0", bg="#dddddd", font=("rockwell", 20))
        self.label_suma_total.place(x=405, y=395)
    
    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            if not productos:
                print("No se encontraron productos en la base de datos")
            conn.close
        except sqlite3.Error as e:
            print("Error al cargar productos desde la base de datos:", e)
    
    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre_producto,))
            precio = c.fetchone()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio[0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el precio: {e}")
        finally:
            conn.close()
            
    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values") [3])
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: ${total:.0f}")
        
    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()
        
        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error", "Stock insuficiente para el producto seleccionado")
                    return
                precio = float(precio)
                subtotal = cantidad*precio
                self.tree.insert("", "end", values=(producto, f"{precio:.0f}", cantidad, f"{subtotal:.0f}"))
                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)
                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error", "Cantidad o precio no validos")
        else:
            messagebox.showerror("Advertencia", "Todos los campos son obligatorios")
    
    def verificar_stock(self, nombre_producto, cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c =  conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre_producto,))
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close()
    
    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values") [3])
            total += subtotal
        return total
    
    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay articulos para pagar")
            return
        
        ventana_pago = Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400")
        ventana_pago.config(bg="#dddddd")
        ventana_pago.resizable(False, False)
        
        label_total = tk.Label(ventana_pago, bg="#dddddd", text=f"Total a pagar: ${self.obtener_total():.0f}", font=("rockwell", 18))
        label_total.place(x=70, y=20)
        
        label_cantidad_pagada = tk.Label(ventana_pago, bg="#dddddd", text="Cantidad pagada:", font=("rockwell", 12))
        label_cantidad_pagada.place(x=120, y=100)
        entry_cantidad_pagada = ttk.Entry(ventana_pago, font=("rockwell", 12))
        entry_cantidad_pagada.place(x=80, y=140, width=240, height=30)
        
        label_cambio = tk.Label(ventana_pago, bg="#dddddd", text="", font=("rockwell", 12))
        label_cambio.place(x=100, y=190)
        
        def calcular_cambio():
            try:
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total
                if cambio < 0:
                    messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                    return
                label_cambio.config(text=f"Vuelto: ${cambio:.0f}")
            except ValueError:
                messagebox.showerror("Error", "Cantidad pagada no valida")
                
        boton_calcular = tk.Button(ventana_pago, text="Calcular vuelto", bg="#959595", font=("rockwell", 12), command=calcular_cambio)
        boton_calcular.place(x=80, y=260, width=240, height=40)
        
        boton_pagar = tk.Button(ventana_pago, text="Pagar", bg="#959595", font=("rockwell", 12), command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio))
        boton_pagar.place(x=80, y=320, width=240, height=40)
        
    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio < 0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                return
            conn =  sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    nombre_producto = item[0]
                    cantidad_vendida = int(item[2])
                    if self.verificar_stock(nombre_producto, cantidad_vendida):
                        cantidad_vendida = int(item[2])
                        precio_venta = float(item[1])  
                        subtotal = cantidad_vendida * precio_venta
                        c.execute("INSERT INTO ventas (nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?, ?, ?, ?)", 
                                    (nombre_producto, precio_venta, cantidad_vendida, subtotal))
                        c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad_vendida, nombre_producto))
                    else:
                        messagebox.showerror("Error", f"Stock insuficiente para el producto: {nombre_producto}")
                    
                conn.commit()
                messagebox.showinfo("Exito", "Venta registrada exitosamente")
                
                ventana_pago.destroy()
                
            except sqlite3.Error as e:
                conn.rollback
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")
            finally:
                conn.close()
        
        except ValueError:
            messagebox.showerror("Error", "Cantidad pagada no valida")