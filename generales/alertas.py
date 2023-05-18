from customtkinter import CTkToplevel
from tkinter import messagebox
from updater.update_checker import check
from archivos.dppsv.get_info import Datos

class Alerts:

    def __init__(self) -> None:
        pass

    def informacion(mensaje:str) -> None:
        messagebox.showinfo(
            title='Alerta de estado',
            message= f'Se finalizo el proceso. {mensaje}',
            )
        

    def informacion_dppsv(mensaje:str, txt:str) -> None:
        datos = Datos()
        cantidad_txt = datos.get_cantidades_finales(txt)
        messagebox.showinfo(
            title='Alerta de estado',
            message= f'Se finalizo el proceso. {mensaje} \nCantidad final en txt: {cantidad_txt}',
            )
    
    
    def aviso_actualizacion(current_version:str) -> bool:
        if check(current_version):
            pregunta = messagebox.askyesno('update', 'Hay una actualizacion disponible.\n Desea descargar la nueva version?')
            return pregunta
        

    def check_actualizacion(current_version:str, top_level:CTkToplevel):
        
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

