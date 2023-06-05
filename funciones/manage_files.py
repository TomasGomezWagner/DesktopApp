import os
import csv

class Manage:

    def __init__(self) -> None:
        pass


    def leer_archivo(ruta_archivo:str) -> list:

        datos_csv = []
        with open(ruta_archivo, 'r', encoding='latin1') as file:
            reader = csv.reader(file, delimiter=';')
            for item in reader:
                datos_csv.append(item)
        file.close()
        return datos_csv


    def make_archivo(registros:list[list], ruta:str) -> None:
        
        with open(ruta, 'w', encoding='latin1', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for row in registros:
                writer.writerow(row)

        file.close()

    
    def hacer_carpeta_temp(ruta) -> None:
        """Si no existe la carpeta, la crea"""
        if not os.path.isdir(ruta):
            os.mkdir(ruta)

        




if __name__=='__main__':

    

    Manage.hacer_carpeta_temp(r'C:\Users\user\Desktop\lalolanda')