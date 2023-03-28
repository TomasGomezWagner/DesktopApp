from tkinter import messagebox
from updater.update_checker import check

class Alerts:

    def __init__(self) -> None:
        pass

    def informacion(mensaje:str):
        messagebox.showinfo(
            title='Alerta de estado',
            message= f'Se finalizo el proceso. {mensaje}',
            )
    
    def aviso_actualizacion(current_version):
        if check(current_version):
            pregunta = messagebox.askyesno('update', 'Hay una actualizacion disponible.\n Desea descargar la nueva version?')
            return pregunta
        

    def check_actualizacion(current_version, top_level):
        
        if check(current_version):
            
            top_level.destroy()
            pregunta = messagebox.askyesno('update', 'Hay una actualizacion disponible.\n Desea descargar la nueva version?')
            return pregunta

        else:
            top_level.destroy()
            messagebox.showinfo('update', 'Ya tiene la version mas reciente del programa.')
    


    def informacion_actualizacion(root):
        messagebox.showinfo(
            title='Alerta de estado',
            message='Se finalizo el proceso de actualizacion',
            )
        root.destroy()

