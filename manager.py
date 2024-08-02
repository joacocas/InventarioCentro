from tkinter import Tk, Frame
from container import Container
from ttkthemes import ThemedStyle
import sys
import os

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventario Centro[*]")
        self.resizable(False, False)
        self.configure(bg="white")
        self.geometry("800x400+120+20")
        ruta=self.rutas(r"CentroLogo.ico")
        self.iconbitmap(ruta)
        
        #Contenedor
        self.container = Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)
        
        #Diccionario
        self.frames = {
            Container: None
        }
        
        self.load_frames()
        self.show_frame(Container)
        self.set_theme()
        
    def rutas(self, ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase, ruta)
    
    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
    
    def set_theme(self):
        style = ThemedStyle(self)
        style.set_theme("adapta")
        
def main():
    app = Manager()
    app.mainloop()
    
if __name__ == "__main__":
    root = Tk()
    app = Container(master=root)
    app.mainloop()