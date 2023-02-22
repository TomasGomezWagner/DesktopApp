
import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from rutas import examinar
from rutas import examinar_carpeta
from funciones_principales import Principales
from alertas import Alerts
from top_level_info import ToplevelWindow
from settings import VERSION

class VistaPrincipal(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.chek_version = Alerts.aviso_actualizacion(VERSION)

        self.ico = Image.open(os.path.join(os.getcwd(), 'img', 'log_cecaitra.png'))
        self.foto = ImageTk.PhotoImage(self.ico)
        self.wm_iconphoto(False, self.foto)

        self.title('Revision')
        self.geometry('500x500')
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.toplevel_window = None

        # ------------------------------------------------------------------------

        # ------------------------      MENU      --------------------------------

        # ------------------------------------------------------------------------


        self.barra_menu = tk.Menu(self)
        self.info = tk.Menu(self.barra_menu, tearoff=False)
        self.barra_menu.add_command(label='Informacion', command=lambda:self.open_toplevel())
        self.config(menu=self.barra_menu)

        # ------------------------------------------------------------------------

        # ------------------      FRAME IZQUIERDA      ---------------------------

        # ------------------------------------------------------------------------

        self.frame_izquierda = customtkinter.CTkFrame(self,)
        self.frame_izquierda.grid(column=0, row=0, sticky='nsew')

        self.imagen = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(os.getcwd(), 'img', 'log_cecaitra.png')),
            light_image=Image.open(os.path.join(os.getcwd(), 'img','logo_cecaitra_negro.png')),
            size=(100,100),
            )
        self.label_img = customtkinter.CTkLabel(self.frame_izquierda, image=self.imagen, text='')
        self.label_img.grid(column=0, row=0)

        self.label_titulo = customtkinter.CTkLabel(
            self.frame_izquierda,
            text="REVISION",
            )
        self.label_titulo.grid(column=0,row=1, pady=20, padx=20)

        self.txt_btn = customtkinter.CTkButton(self.frame_izquierda, text='Filtrar txt', command=self.frame_txt)
        self.txt_btn.grid(column=0, row=2, pady=10, padx=10)
        self.txt_btn = customtkinter.CTkButton(self.frame_izquierda, text='Filtrar imagenes', command=self.frame_img)
        self.txt_btn.grid(column=0, row=3, pady=10, padx=10)

        self.switch_var = customtkinter.StringVar(value='on')
        swich = customtkinter.CTkSwitch(self.frame_izquierda, text='Cambiar color', command=self.switch_event, variable=self.switch_var, onvalue='on', offvalue='off')
        swich.grid(column=0, row=5, pady=10, padx=10)

        # ------------------------------------------------------------------------

        # ---------------------      FRAME BIENVENIDA     ------------------------

        # ------------------------------------------------------------------------

        self.bienvenido = customtkinter.CTkLabel(
            self,
            text='BIENVENIDOS AL SISTEMA DE REVISION\n DE CSV DE LA PROVINCIA',
            )
        self.bienvenido.grid(column=1, row=0)

        # ------------------------------------------------------------------------

        # ------------------------      FRAME TXT      ---------------------------

        # ------------------------------------------------------------------------

    def frame_txt(self,):
        self.frame_derecha_txt = customtkinter.CTkFrame(self)
        self.frame_derecha_txt.grid(column=1, row=0, pady=10, padx=10, sticky='nsew')
        self.frame_derecha_txt.grid_columnconfigure(0, weight=1)
        self.frame_derecha_txt.grid_rowconfigure(4, weight=1)

        self.subtitulo = customtkinter.CTkLabel(self.frame_derecha_txt, text='FILTRAR ARCHIVO')
        self.subtitulo.grid(column=0, row=0, pady=10, padx=10, sticky='ew')

        self.ruta_txt = customtkinter.StringVar()
        self.entry_ruta = customtkinter.CTkEntry(self.frame_derecha_txt, textvariable=self.ruta_txt)
        self.entry_ruta.grid(column=0, row=2, pady=20, padx=20, sticky='ew')

        self.btn_examinar = customtkinter.CTkButton(self.frame_derecha_txt, text='EXAMINAR', command=lambda:examinar(self.ruta_txt))
        self.btn_examinar.grid(column=0, row=3, pady=20, padx=50, sticky='ew')

        self.btn_procesar = customtkinter.CTkButton(self.frame_derecha_txt, text='PROCESAR', command=lambda:Principales.filtrar_archivo_txt(self.ruta_txt.get()))
        self.btn_procesar.grid(column=0, row=5, pady=20, padx=20, sticky='ew')

        return self.frame_derecha_txt


        # ------------------------------------------------------------------------

        # ------------------------      FRAME IMG      ---------------------------

        # ------------------------------------------------------------------------

    def frame_img(self,):
        self.frame_derecha_img = customtkinter.CTkFrame(self)
        self.frame_derecha_img.grid(column=1, row=0, pady=10, padx=10, sticky='nsew')
        self.frame_derecha_img.grid_columnconfigure(0, weight=1)
        self.frame_derecha_img.grid_rowconfigure((7), weight=1)

        self.subtitulo = customtkinter.CTkLabel(self.frame_derecha_img, text='FILTRAR IMAGENES')
        self.subtitulo.grid(column=0, row=0, pady=10, padx=10, sticky='ew')

        self.label_txt = customtkinter.CTkLabel(self.frame_derecha_img, text='Ruta del archivo de descartes', anchor='w')
        self.label_txt.grid(column=0, row=1, padx=20, sticky='ew')

        self.ruta_descarte = customtkinter.StringVar()
        self.entry_ruta_txt_descarte = customtkinter.CTkEntry(self.frame_derecha_img, textvariable=self.ruta_descarte)
        self.entry_ruta_txt_descarte.grid(column=0, row=2, pady=(10,5), padx=20, sticky='ew')

        self.btn_examinar = customtkinter.CTkButton(self.frame_derecha_img, text='EXAMINAR', command=lambda:examinar(self.ruta_descarte))
        self.btn_examinar.grid(column=0, row=3, pady=(5,10), padx=50, sticky='ew')

        self.label_txt = customtkinter.CTkLabel(self.frame_derecha_img, text='Ruta de la carpeta de imagenes', anchor='w')
        self.label_txt.grid(column=0, row=4, pady=(30,0), padx=20, sticky='ew')

        self.ruta_img = customtkinter.StringVar()
        self.entry_ruta = customtkinter.CTkEntry(self.frame_derecha_img, textvariable=self.ruta_img)
        self.entry_ruta.grid(column=0, row=5, pady=(10,5), padx=20, sticky='ew')

        self.btn_examinar_carpeta = customtkinter.CTkButton(self.frame_derecha_img, text='EXAMINAR', command=lambda:examinar_carpeta(self.ruta_img))
        self.btn_examinar_carpeta.grid(column=0, row=6, pady=(5,10), padx=50, sticky='ew')

        self.btn_procesar = customtkinter.CTkButton(
            self.frame_derecha_img,
            text='PROCESAR',
            command=lambda:Principales.filtrar_img(
                self.ruta_img.get(),
                self.ruta_descarte.get(),
                )
        )
        self.btn_procesar.grid(column=0, row=8, pady=20, padx=20, sticky='ew')

        return self.frame_derecha_img


    def switch_event(self,):
        if self.switch_var.get() == 'on':
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def open_toplevel(self,):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self, self,)




if __name__ == "__main__":

    from actualizador_vista import Actualizador

    app = VistaPrincipal()
    if app.chek_version == True:
        app.destroy()
        asd = Actualizador()
        asd.focus_force()
        asd.mainloop()
    else:
        app.mainloop()
