from tkinter import messagebox
from update_checker import check

class Alerts:

    def __init__(self) -> None:
        pass

    def informacion():
        messagebox.showinfo(
            title='Alerta de estado',
            message='Se finalizo el proceso',
            )
    
    def aviso_actualizacion(current_version):
        if check(current_version):
            messagebox.showinfo('update', 'hay una actualizacion')
        

    def check_actualizacion(current_version, top_level):
        if check(current_version):
            top_level.destroy()
            messagebox.showinfo('update', 'hay una actualizacion')
        else:
            top_level.destroy()
            messagebox.showinfo('update', 'Ya tiene la version mas reciente del programa.')
