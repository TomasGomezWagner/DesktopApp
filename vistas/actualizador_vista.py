from tkinter import *
from generales.rutas import examinar_carpeta
from updater.descarga_ftp import actualizar_app

class Actualizador(Tk):
    def __init__(self,) -> None:
        super().__init__()

        self.title('Actualizador')
        self.geometry('400x300')
        self.grid_columnconfigure(0, weight=1)
        self.destino = StringVar()

        self.titulo = Label(self, text='ACTUALIZADOR App')
        self.titulo.grid(column=0, row=1)

        self.eleccion = Label(self, text='Elija la carpeta donde se instalara la applicacion')
        self.eleccion.grid(column=0, row=2, pady=(20,5))

        self.ruta_destino = Entry(self, textvariable=self.destino)
        self.ruta_destino.grid(column=0, row=3,padx=20, sticky='we')

        self.boton = Button(self, text='Buscar carpeta', command=lambda:examinar_carpeta(self.destino))
        self.boton.grid(column=0, row=4, pady=(10,20))

        self.actualizar = Button(self, text='Actualizar',background='green', command=lambda:actualizar_app(self.destino.get(), self))
        self.actualizar.grid(column=0, row=5, pady=20, padx=20, sticky='we')

        self.boton_cerrar = Button(text='Cerrar', command=lambda:self.quit())
        self.boton_cerrar.grid(column=0, row=6, pady=10, padx=20, sticky='e')


# if __name__ == '__main__':
#     app = Actualizador()
#     app.mainloop()