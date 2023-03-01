import platform
import os
from ftplib import FTP
from generales.alertas import Alerts
from updater.make_shurtcut import make_shortcut

def is_ftp_dir(ftp_handle:FTP, name, guess_by_extension=True):
    """ Determina si un item listado en el servidor ftp es un directorio valido o no """

    # si el nombre tiene "." en la cuarta posicion desde el final, es probablemente un archivo
    # esto es MUCHO mas rapido que setear cada archivo como un directorio valido, y funcionara el 99% de las veces.

    if guess_by_extension is True:
        if name[-4] == '.':
            return False
        elif name[-3] == '.':
            return False

    original_cwd = ftp_handle.pwd()
    try:
        ftp_handle.cwd(name)
        ftp_handle.cwd(original_cwd)
        return True
    except:
        return False

def make_parents(origen:str, dest:str, ruta:str):
    """ 
    Toma la ruta del item listado y lo compara con la ruta base del ftp. Obtiene las carpetas\n
    que sobran de la ruta del item e intenta crearlas.
    """
    origen_items    = origen.split('/')
    ruta_items      = ruta.split('/')

    directorios_extra = [x for x in ruta_items if x not in origen_items]

    for item in directorios_extra:
        dest = os.path.join(dest, item)
        try:
            os.mkdir(dest)
            print('Carpeta creada: {0}'.format(dest))
        except FileExistsError:
            print('carpeta ya existe: {0}'.format(dest))
        except Exception as e:
            print(e)

def descargar_archivo(ftp:FTP, origen:str, destino:str, sobreecribir):
    """ Descarga un archivo del ftp a la carpeta destino """

    if not os.path.exists(destino) or sobreecribir is True:
        with open(destino, 'wb') as f:
            ftp.retrbinary("RETR {0}".format(origen), f.write)
        print('Descargado: {0}'.format(origen))
    else:
        print('Ya existe en destino: {0}'.format(origen))
            

def crear(ftp:FTP, dir_base_linux:str, dest:str, guess_by_extension=True, sobreescribir=True):
    """
    Descarga un directorio completo desde un servidor ftp de linux a una carpeta en windows (deberia funcionar\n
    en linux tambien, testear)
    
    """
    for item in ftp.nlst(dir_base_linux):   

        new_dest = dest
        
        if is_ftp_dir(ftp, item, guess_by_extension):
            make_parents(dir_base_linux, dest, item)
            dir_base_linux = item
            new_dest = os.path.join(dest, dir_base_linux.split('/')[-1])
            crear(ftp, dir_base_linux, new_dest)
        else:
            print(f'{item=}')
            base, nombre = os.path.split(item)
            destino = os.path.join(new_dest, nombre)
            descargar_archivo(ftp, item, destino, sobreescribir)



def actualizar_app(dest:str, root, guess_by_extension=True, sobreescribir=True):

    ftp = FTP(host='192.168.3.232', user='cecaitra', passwd='Haiti1688')

    os_type = platform.system()
    print(f'Descargando la nueva version para el sistema operativo {str(os_type).upper()}')

    if os_type == 'Windows':
        dir_base_fuente = '/home/cecaitra/versiones/win'
        dir_base_fuente = ftp.nlst(dir_base_fuente)[-1]
        crear(ftp, dir_base_fuente, dest, guess_by_extension, sobreescribir)
        make_shortcut(dest, name='Procesos')
        Alerts.informacion_actualizacion(root)

    elif os_type == 'Linux':
        dir_base_fuente = '/home/cecaitra/versiones/linux'
        dir_base_fuente = ftp.nlst(dir_base_fuente)[-1]
        crear(ftp, dir_base_fuente, dest)
        Alerts.informacion_actualizacion(root)














#ftp = FTP(host='192.168.3.232', user='cecaitra', passwd='Haiti1688')


# mirror(
#     ftp, 
#     path='/home/cecaitra/proyecto',
#     destino=r'C:\Users\hcapra\Desktop\asd',
#     sobreescribir=True,
#     guess_by_extension=False,
# )


# download_ftp_file(
#     ftp,
#     path_src='/home/cecaitra/proyecto/__pycache__/alertas.cpython-39.pyc',
#     dest=r'C:\Users\hcapra\Desktop\asd',
#     sobreescribir=False,
# )

# make_parent_dir('/home/cecaitra/proyecto/__pycache__/asd/qwe/alertas.cpython-39.pyc', r'C:\Users\hcapra\Desktop\asd')


