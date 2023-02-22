import urllib.request
from settings import RUTA_VERSION


def check(current_version):
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
        
