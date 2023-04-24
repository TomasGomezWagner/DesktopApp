
import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from funciones.funciones_principales import Principales
from generales.alertas import Alerts
from vistas.top_level_info import ToplevelWindow
from generales.rutas import examinar
from generales.rutas import examinar_carpeta
from dppsv.funciones_principales import igual_o_diferente
from generales.settings import VERSION

from vistas.progress_bar import TopLevelProgressBar

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
        self.frame_izquierda.grid_rowconfigure(5, weight=1)
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
        self.img_btn = customtkinter.CTkButton(self.frame_izquierda, text='Filtrar imagenes', command=self.frame_img)
        self.img_btn.grid(column=0, row=3, pady=10, padx=10)
        self.img_btn = customtkinter.CTkButton(self.frame_izquierda, text='DPPSV', command=self.frame_dppsv)
        self.img_btn.grid(column=0, row=4, pady=10, padx=10)

        self.switch_var = customtkinter.StringVar(value='on')
        swich = customtkinter.CTkSwitch(self.frame_izquierda, text='Cambiar color', command=self.switch_event, variable=self.switch_var, onvalue='on', offvalue='off')
        swich.grid(column=0, row=6, pady=10, padx=10)

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

        self.ruta_txt = customtkinter.StringVar()

        self.subtitulo = customtkinter.CTkLabel(self.frame_derecha_txt, text='FILTRAR ARCHIVO')
        self.subtitulo.grid(column=0, row=0, pady=10, padx=10, sticky='ew')

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

        self.ruta_descarte  = customtkinter.StringVar()
        self.ruta_img       = customtkinter.StringVar()

        self.subtitulo = customtkinter.CTkLabel(self.frame_derecha_img, text='FILTRAR IMAGENES')
        self.subtitulo.grid(column=0, row=0, pady=10, padx=10, sticky='ew')

        self.label_txt = customtkinter.CTkLabel(self.frame_derecha_img, text='Ruta del archivo de descartes', anchor='w')
        self.label_txt.grid(column=0, row=1)

        self.entry_ruta_txt_descarte = customtkinter.CTkEntry(self.frame_derecha_img, textvariable=self.ruta_descarte)
        self.entry_ruta_txt_descarte.grid(column=0, row=2, pady=(10,5), padx=20, sticky='ew')

        self.btn_examinar = customtkinter.CTkButton(self.frame_derecha_img, text='EXAMINAR', command=lambda:examinar(self.ruta_descarte))
        self.btn_examinar.grid(column=0, row=3, pady=(5,10), padx=50, sticky='ew')

        self.label_txt = customtkinter.CTkLabel(self.frame_derecha_img, text='Ruta de la carpeta de imagenes', anchor='w')
        self.label_txt.grid(column=0, row=4, pady=(30,0))
        
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
    
    
    # ------------------------------------------------------------------------

    # ------------------     FRAME DEVOLUCION DPPSV     ----------------------

    # ------------------------------------------------------------------------

    def frame_dppsv(self,):
        self.frame_derecha_dppsv = customtkinter.CTkFrame(self)
        self.frame_derecha_dppsv.grid(column=1, row=0, pady=10, padx=10, sticky='nsew')
        self.frame_derecha_dppsv.grid_columnconfigure(0, weight=1)
        self.frame_derecha_dppsv.grid_rowconfigure(7, weight=1)

        self.pdfs_dppsv  = customtkinter.StringVar()
        self.txt_dppsv   = customtkinter.StringVar()

        self.titulo_lbl = customtkinter.CTkLabel(self.frame_derecha_dppsv, text='DEVOLUCION DPPSV')
        self.titulo_lbl.grid(column=0, row=0, pady=10)

        self.label_txt = customtkinter.CTkLabel(self.frame_derecha_dppsv, text='Ruta del archivo txt')
        self.label_txt.grid(column=0, row=1)
        self.entry_txt = customtkinter.CTkEntry(self.frame_derecha_dppsv, textvariable=self.txt_dppsv)
        self.entry_txt.grid(column=0, row=2, sticky='we', padx=20)
        self.btn_txt = customtkinter.CTkButton(self.frame_derecha_dppsv, text='examinar', command=lambda:examinar(self.txt_dppsv))
        self.btn_txt.grid(column=0, row=3, sticky='we', padx=70, pady=10)

        self.label_pdf = customtkinter.CTkLabel(self.frame_derecha_dppsv, text='Ruta de carpeta de PDF')
        self.label_pdf.grid(column=0, row=4)
        self.entry_pdf = customtkinter.CTkEntry(self.frame_derecha_dppsv, textvariable=self.pdfs_dppsv)
        self.entry_pdf.grid(column=0, row=5, sticky='we', padx=20)
        self.btn_pdf = customtkinter.CTkButton(self.frame_derecha_dppsv, text='examinar', command=lambda:examinar_carpeta(self.pdfs_dppsv))
        self.btn_pdf.grid(column=0, row=6, sticky='we', padx=70, pady=10)

        self.btn_procesar = customtkinter.CTkButton(
            self.frame_derecha_dppsv,
            text='PROCESAR',
            # command=lambda:igual_o_diferente(self.txt_dppsv.get(), self.pdfs_dppsv.get()),
            # )
            command=lambda:self.open_toplevel_progress())
        self.btn_procesar.grid(column=0, row=8, pady=20, padx=20, sticky='ew')

        return self.frame_derecha_dppsv
        
#-------------------------------------------------------------------------------------------------------------------

    def switch_event(self,):
        if self.switch_var.get() == 'on':
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def open_toplevel(self,):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self, self,)

    def open_toplevel_progress(self,):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelProgressBar(self.txt_dppsv.get(),self.pdfs_dppsv.get())




if __name__ == "__main__":

    from vistas.actualizador_vista import Actualizador

    app = VistaPrincipal()
    if app.chek_version == True:
        app.destroy()
        asd = Actualizador()
        asd.focus_force()
        asd.mainloop()
    else:
        app.mainloop()
