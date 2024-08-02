from tkinter import Frame, Tk, Button, Label
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk
import sys
import os

class Container(Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x = 0, y = 0, width = 800, height = 400)
        self.config(bg="#dddddd")
        self.widgets()
    
    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase, ruta)
        
    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#dddddd")
        frame.pack(fill = "both", expand = True)
        top_level.geometry("1100x650+120+20")
        top_level.resizable(False, False)
        ruta=self.rutas(r"CentroLogo.ico")
        top_level.iconbitmap(ruta)
        
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()
    
    def ventas(self):
        self.show_frames(Ventas)
    
    def inventario(self):
        self.show_frames(Inventario)
        
    def widgets(self):
        frame1 = tk.Frame(self, bg="white")
        frame1.pack()
        frame1.place(x= 0, y=0, width=800, height=400)
        
        #Boton ventas
        btnventas = Button(frame1, bg="#959595", fg="black", font="rockwell 15", text="VENTAS", command=self.ventas)
        btnventas.place(x= 500, y=100, width=240, height=60)
        
        #Boton inventario
        btninventario = Button(frame1, bg="#959595", fg="black", font="rockwell 15", text="INVENTARIO", command=self.inventario)
        btninventario.place(x= 500, y=200, width=240, height=60)
        
        #Imagen logo
        self.logo_image = Image.open("Imagenes/CentroLogo.PNG")
        self.logo_image = self.logo_image.resize((280,280))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="white")
        self.logo_label.place(x=100, y=50)
        
        #Copyright
        copyright_label = tk.Label(frame1, text="© 2024 joacocas code. Todos los derechos reservados", font="sans 12 bold", bg="white", fg="gray")
        copyright_label.place(x=180, y=350)