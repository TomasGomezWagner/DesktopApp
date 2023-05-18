import os
from PIL import Image
import customtkinter
from generales.alertas import Alerts
from generales.settings import VERSION
from vistas.actualizador_vista import Actualizador

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, padre, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padre = padre

        self.title('About')
        self.geometry("300x300")
        self.grid_columnconfigure((0,5), weight=1)

        self.imagen = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(os.getcwd(), 'img', 'log_cecaitra.png')),
            light_image=Image.open(os.path.join(os.getcwd(), 'img','logo_cecaitra_negro.png')),
            size=(100,100),
            )
        self.label_img = customtkinter.CTkLabel(self, image=self.imagen, text='')
        self.label_img.grid(column=0, row=0)

        self.label_titulo = customtkinter.CTkLabel(self, text="Informacion del programa")
        self.label_titulo.grid(column=0, row=1, sticky='w', padx=50)
        
        self.label_version = customtkinter.CTkLabel(self, text=f"Version: {VERSION}")
        self.label_version.grid(column=0, row=2, sticky='w', padx=50)
        
        self.label_empresa = customtkinter.CTkLabel(self, text=f"Empresa: CECAITRA")
        self.label_empresa.grid(column=0, row=3, sticky='w', padx=50)

        self.label_coder = customtkinter.CTkLabel(self, text="Desarrollador: Tomas Wagner")
        self.label_coder.grid(column=0, row=4, sticky='w', padx=50)

        self.boton = customtkinter.CTkButton(
            self,
            text="Verificar Actualizaciones",
            command=lambda:self.actualizar(),
            )
        self.boton.grid(column=0, row=5, pady=20)
    

    def actualizar(self, ) -> None:
        pregunta = Alerts.check_actualizacion(VERSION, self)
        if pregunta:
            self.quit()
            self.padre.destroy()
            actualizador = Actualizador()
            actualizador.mainloop()

