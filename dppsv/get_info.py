import os 
import glob
import csv
import shutil
import datetime
from pathlib import Path

from archivos.funciones.manage_files import Manage


class Datos:

    def __init__(self) -> None:
        pass


    def nombres_pdf(self, ruta_pdfs:str) -> list:
        """ Devuelve una lista con solamente los nombres de los PDF unicos. """

        nombres_pdfs    = []
        unicos          = []
        pdfs = glob.glob(os.path.join(ruta_pdfs, '*.pdf'))

        for item in pdfs:
            head, pdf = os.path.split(item)
            nombres_pdfs.append(pdf.split('_')[1])
        
        [x for x in nombres_pdfs if x not in unicos and (unicos.append(x) or True)] #obtengo solo los unicos

        return unicos


    def nombres_txt(self, ruta_txt:str) -> list:
        """ Devuelve una lista con los TODOS los nombres de PDF unicos que hay en el txt """

        nombres_txt = []
        unicos      = []

        with open(ruta_txt, 'r', encoding='latin-1') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 2 or len(row) == 3:
                    continue
                else:
                    nombres_txt.append(row[1])
        
            file.close()
        
        [x for x in nombres_txt if x not in unicos and (unicos.append(x) or True)] #obtengo solo los unicos
        
        return unicos


    def txt_info(self, ruta_txt:str) -> list:
        """
        Devuelve una lista que tiene dos elementos:\n
        [0] = la cabecera del txt\n
        [1] = el contenido del txt menos la ultima linea(cantidad)
        """

        info_txt = []
        cabecera = []
        contador = 0

        with open(ruta_txt, 'r', encoding='latin-1') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if contador == 0:
                    cabecera.append(row)
                else:
                    info_txt.append(row)

                contador += 1

        return [cabecera, info_txt[:-1]]


    def filtrar_txt_nuevo(self, ruta_txt:str, ruta_pdfs:str) ->list:
        """
        Devuleve la informacion del txt sin repetidos y que esten en la lista de pdfs unicos.\n
        La cabecera se obtiene en txt_info.\n
        Retorna una lista:\n
        [0] = solo los numeros de pdf unicos\n
        [1] = lista de lista con todas las lineas del txt que corresponden.
        """
        registros_unicos    = []
        info_final          = []
        info                = self.txt_info(ruta_txt)[1]
        unicas              = self.nombres_txt(ruta_txt)
        pdf_unicos          = self.nombres_pdf(ruta_pdfs) 
        

        for registro_unico in unicas:
            for line in info:
                if line[1] == registro_unico and registro_unico in pdf_unicos:
                    info_final.append(line)
                    registros_unicos.append(registro_unico)
                    break
        
        return [registros_unicos, info_final]


    def generar_txt(self, ruta_txt:str, ruta_pdfs:str) -> None:
        """Recibe la ruta del txt original y genera el txt con la informacion correcta,\n
        sin repetidos, que esten en la lista de archivos pdf y con el sufijo "_FILTRADO".
        """

        cabecera        = self.txt_info(ruta_txt)[0]
        info            = self.filtrar_txt_nuevo(ruta_txt, ruta_pdfs)[1]
        padre, archivo  = os.path.split(ruta_txt)
        archivo         = archivo[:-4]
        nuevo_txt       = os.path.join(padre, f'{archivo}_filtrado.txt')
        
        with open(nuevo_txt, 'w', newline="", encoding='latin-1') as file:
            writer = csv.writer(file, delimiter=';')
            cabecera = [cabecera[0][0],cabecera[0][1],'']
            writer.writerow(cabecera)
            for line in info:
                writer.writerow(line)
            writer.writerow(['F',len(info),''])
            
        file.close()


    def mas_pdf(self, nombres_pdf:list, nombres_txt:list, ruta_pdf:str) -> None:
        """
        Separa, en una carpeta "pdf_demas", los PDFs que no estan en la lista de nombres unicos del txt.\n
        NOMBRES_PDF = lista de los numeros de acta de los pdf.\n 
        NOMBRES_TXT = lista de numeros de acta en el txt.\n
        RUTA_PDF = ruta de la carpeta donde se alojan los pdf.
        """
        a_separar = []
        for pdf in nombres_pdf:
            if pdf not in nombres_txt:
                a_separar.append(pdf)
        
        nueva_carpeta = os.path.join(ruta_pdf, 'pdf_demas')
        os.mkdir(nueva_carpeta)
        
        rutas = glob.glob(os.path.join(ruta_pdf, '*.pdf'))

        for item in a_separar:
            for ruta in rutas:
                head, archivo = os.path.split(ruta)
                if archivo.split('_')[1] == item:
                    shutil.move(
                    os.path.join(ruta),
                    os.path.join(nueva_carpeta, archivo)
                    )
            

    def mas_txt(self, ruta_txt:str, nombres_pdf:list) -> None:
        """
        RUTA_TXT = ruta del archivo txt original.\n
        NOMBRES_PDF = lista generada de los nombres de acta de los pdf.\n
        """
        head, archivo               = os.path.split(ruta_txt)
        archivo_filtrado_primero    = os.path.join(head, f'{archivo[:-4]}_filtrado.txt')
        archivo_final               = os.path.join(head, f'{archivo[:-4]}_final.txt')
        
        nuevos_datos = Manage.leer_archivo(archivo_filtrado_primero)

        nuevos_datos.pop(-1)
        contador = 0

        with open(archivo_final, 'w', encoding='latin-1', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for row in nuevos_datos:
                if nuevos_datos.index(row) == 0:
                    writer.writerow(row)
                else:
                    if row[1] in nombres_pdf:
                        writer.writerow(row)
                        contador += 1
            writer.writerow(['F',str(contador), ''])
        file.close()

    
    def renombrar_filtrado(self, ruta_txt:str) -> None:
        
        head, nombre    = os.path.split(ruta_txt)
        nombre          = nombre.split('.')[0]
        ruta_filtrado   = os.path.join(head, f'{nombre}_filtrado.txt')
        ruta_final      = os.path.join(head, f'{nombre}_final.txt')

        os.rename(ruta_filtrado, ruta_final)

    
    def renombrar_archivos_txt(self, ruta_txt:str, tipo_de_proceso:str) -> None:
        base, archivo_fuente    = os.path.split(ruta_txt)
        archivo_fuente          = archivo_fuente.split('.')[0]
        nuevo_original          = os.path.join(base, f'{archivo_fuente}_original.txt')
        nuevo_sin_sufijo        = os.path.join(base, f'{archivo_fuente}.txt')
        os.rename(ruta_txt, nuevo_original)

        #filtrado_a_final
        if (tipo_de_proceso == 'iguales' or tipo_de_proceso == 'pdf'):  

            src = os.path.join(base, f'{archivo_fuente}_filtrado.txt')
            os.rename(src, nuevo_sin_sufijo)

        #final_a_sin_sufigo
        if tipo_de_proceso == 'txt': 

            src = os.path.join(base, f'{archivo_fuente}_final.txt')
            os.remove(os.path.join(base, f'{archivo_fuente}_filtrado.txt'))
            os.rename(src, nuevo_sin_sufijo)
        

    def get_diferencia(self, txt:list, pdf:list) -> bool:
        """
        True: txt tiene mas cantidad.
        False: pdf tiene mas cantidad\n
        """
        if len(txt) > len(pdf):
            return True
        else:
            return False


    def get_cantidades_finales(self, ruta_txt:str) -> int:
        """
        Devuelve las cantidades finales de txt (lo obtiene del ultimo archivo generado\n
        que queda con el nombre del archivo original, sin extencion).
        """
        head, archivo           = os.path.split(ruta_txt)
        cantidad_archivo_txt    = len(Manage.leer_archivo(os.path.join(head, archivo))) - 2

        return cantidad_archivo_txt   



    def pasar_a_carpeta_temp(self, rc:str) -> None:

        carpeta_temp                = r'c:\Temp'
        carpeta_rc                  = Path(rc).resolve().parent
        ruta_txt_salida             = glob.glob(os.path.join(carpeta_rc, '*Salida.txt'))[0]
        dia_de_realizacion          = datetime.datetime.now().date().strftime('%Y%m%d')
        ruta_archivo_salida_temp    = os.path.join(carpeta_temp, f'{dia_de_realizacion}_Salida.txt')
        fecha_txt_salida_original   = os.path.basename(ruta_txt_salida).split('-')[1]

        Manage.hacer_carpeta_temp(carpeta_temp)
        
        if not os.path.exists(ruta_archivo_salida_temp):
            datos           = Manage.leer_archivo(ruta_txt_salida)
            datos_temp      = [[f'1-{fecha_txt_salida_original}']] + datos
            datos_nuevos    = []

            for row in datos_temp:
                if row is not datos_temp[0]:
                    datos_nuevos.append(row + [1])
                else:
                    datos_nuevos.append(row)

            Manage.make_archivo(datos_nuevos, ruta_archivo_salida_temp)
            
        else:
            datos_rc                = Manage.leer_archivo(ruta_txt_salida)
            datos_temp              = Manage.leer_archivo(ruta_archivo_salida_temp)
            ultimio_rc_registrado   = datos_temp[0][-1].split('-')[0]
            datos_temp[0]           = datos_temp[0] + [f'{int(ultimio_rc_registrado)+1}-{fecha_txt_salida_original}']
            datos_temp              = datos_temp + datos_rc
            
            datos_nuevos = []
            for row in datos_temp:
                if (row is not datos_temp[0]) and (not row[-1].isdigit()):
                    row = row + [datos_temp[0][-1].split('-')[0]]
                    datos_nuevos.append(row)
                else:
                    datos_nuevos.append(row)

            Manage.make_archivo(datos_nuevos, ruta_archivo_salida_temp)


    def get_rc_date(self, ruta_rc:str) -> str:

        fecha = ruta_rc.split('_')[-1].split('.')[0]
        return fecha


    def generar_archivo_de_salida(self, ruta_rc:str, pdfs_datos:list[list]) -> None:
        """
        Toma las rutas del archivo RC y la carpeta contenedora de los PDfs\n
        y con los nombres de los PDF crea un archivo txt (SALIDA) que tiene en el nombre\n
        la fecha de realizacion del archivo RC original para poder obtener ese dato\n
        por un modulo en cecasit. 
        """
        pdfs = pdfs_datos
        padre = Path(ruta_rc).resolve().parent
        dia_de_realizacion = datetime.datetime.now().date().strftime('%Y%m%d')
        rc_date = self.get_rc_date(ruta_rc)
        nuevo_archivo = os.path.join(padre, f'{dia_de_realizacion}-{rc_date}-Salida.txt')

        Manage.make_archivo(pdfs, nuevo_archivo)


if __name__ == '__main__':

    asd = Datos()
    
    # nombres_txt = asd.nombres_txt(r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\RC\RC_1000015360_20221010060217.txt')
    # nombres_pdf = asd.nombres_pdf(r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\1000015360')

    # print(asd.igual_o_diferente(
    #     r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\RC\RC_1000015360_20221010060217.txt',
    #     r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\1000015360',
    #     )
    # )
    
    # print(asd.get_diferencia(
    #     r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\xprueba\rc\nuevo.txt',
    #     r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\xprueba\1',
    #     )
    # )
    asd.pasar_a_carpeta_temp(r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\mas_en_pdf\RC\20230516-20221010060217-Salida.txt')