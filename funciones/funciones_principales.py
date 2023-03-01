import os
import glob
import shutil
from funciones.filtros import Filtros
from funciones.manage_files import Manage
from generales.alertas import Alerts

class Principales:
    def __init__(self) -> None:
        pass

    def filtrar_archivo_txt(ruta:str) -> None:

        head, nombre_archivo = os.path.split(ruta)
        nombre_archivo = nombre_archivo.split('.')[0]

        registros = Manage.leer_archivo(ruta)
        filtrar_vacios = Filtros.filtro_vacios(registros)
        filtrar_documento = Filtros.filtro_documento(filtrar_vacios)
        registros_final = Filtros.verificar_sexo(filtrar_documento)

        Manage.make_archivo(registros_final['ok'], os.path.join(head, f'{nombre_archivo}-filtrado.txt'))
        Manage.make_archivo(registros_final['errores'], os.path.join(head, f'{nombre_archivo}-errores.txt'))

        Alerts.informacion()

    def filtrar_img(ruta_imagenes:str, ruta_txt_errores:str) -> None:

        datos_errores       = Manage.leer_archivo(ruta_txt_errores)
        imagenes_a_eliminar = Filtros.get_imagenes_a_borrar(datos_errores)
        imagenes_totales    = glob.glob(os.path.join(ruta_imagenes, '*.jpg'))
        carpeta_elimnadas   = os.path.join(ruta_imagenes, 'ELIMINADAS')
        
        os.mkdir(carpeta_elimnadas)

        for item in imagenes_totales:
            head, nombre_imagen = os.path.split(item)
            if nombre_imagen in imagenes_a_eliminar:
                shutil.move(
                    item,
                    os.path.join(carpeta_elimnadas, nombre_imagen)
                )

        Filtros.modificar_txt_cantidad(ruta_txt_errores)
            
        Alerts.informacion()

