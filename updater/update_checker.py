import urllib.request
from generales.settings import RUTA_VERSION

def check(current_version:str) -> bool:
    """ Devuelve True si la version del repositorio es mas nueva. """

    url = RUTA_VERSION
    file = urllib.request.urlopen(url)
    version = str(file.read())

    version = version[2:-1]
    
    current_version_data = current_version.split('.')
    version_data = version.split('.')

    if current_version == version:
        return False
    
    elif int(version_data[0]) > int(current_version_data[0]):
        return True

    elif (int(version_data[0]) == int(current_version_data[0])): 
        if int(version_data[1]) > int(current_version_data[1]):
            return True
        elif int(version_data[1]) == int(current_version_data[1]):
            if int(version_data[2]) > int(current_version_data[2]):
                return True
            else:
                return False
        

if __name__ == '__main__':
    # para testear la funcion descomentar las importaciones y comentar la importacion de RUTA_VERCION

    # import sys
    # sys.path.insert(0, r'C:\Users\hcapra\Desktop\arreglo_csv\archivos\generales')
    # from settings import RUTA_VERSION
    
    # print(check('1.4.3'))
    pass