import os 
import glob
import csv
import shutil


class Datos:

    def __init__(self) -> None:
        pass

    def nombres_pdf(self, ruta_pdfs:str) -> list:
        """ Devuelve una lista con solamente los nombres de los PDF. """

        nombres_pdfs = []
        pdfs = glob.glob(os.path.join(ruta_pdfs, '*.pdf'))

        for item in pdfs:
            head, pdf = os.path.split(item)
            nombres_pdfs.append(pdf.split('_')[1])
        
        return nombres_pdfs

    def nombres_txt(self, ruta_txt:str) -> list:
        """ Devuelve una lista con los TODOS los nombres de PDF que hay en el txt """

        nombres_txt = []

        with open(ruta_txt, 'r', encoding='latin-1') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 2 or len(row) == 3:
                    continue
                else:
                    nombres_txt.append(row[1])
        
            file.close()
        
        return nombres_txt

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



    def filtrar_txt_nuevo(self, ruta_txt:str) ->list:
        """
        Devuleve la informacion del txt sin repetidos.La cabecera se obtiene en txt_info.\n
        Retorna una lista:\n
        [0] = solo los numeros de pdf unicos\n
        [1] = lista de lista con todas las lineas del txt que corresponden.
        """

        info = self.txt_info(ruta_txt)[1]
        nombres = self.nombres_txt(ruta_txt)
        info_final = []
        repetidas = []
        unicas = []

        contador_dicc = {}

        for item in nombres:
            if item in contador_dicc.keys():
                contador_dicc[item] += 1
            else:
                contador_dicc[item]  = 1

        
        for key, value in contador_dicc.items():
            unicas.append(key)

            if value > 1:
                repetidas.append(key)
            
            for line in info:
                if key == line[1]:
                    info_final.append(line)
                    break
        
        return [unicas, info_final]


    def generar_txt(self, ruta_txt:str) -> None:
        """Recibe la ruta del txt original y genera el txt con la informacion correcta."""

        cabecera = self.txt_info(ruta_txt)[0]
        info = self.filtrar_txt_nuevo(ruta_txt)[1]

        padre, archivo = os.path.split(ruta_txt)
        archivo = archivo[:-4]
        nuevo_txt = os.path.join(padre, f'{archivo}_filtrado.txt')
        
        
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
        head, archivo = os.path.split(ruta_txt) # se cambio archivo_filtrado a archivo
        archivo_filtrado_primero = os.path.join(head, f'{archivo[:-4]}_filtrado.txt')
        archivo_filtrado_segundo = os.path.join(head, f'{archivo[:-4]}_final.txt')
        
        nuevos_datos = []

        with open(archivo_filtrado_primero, 'r', encoding='latin-1') as file:
            reader = csv.reader(file, delimiter=';')
            for line in reader:
                nuevos_datos.append(line)
        file.close()

        nuevos_datos.pop(-1)
        contador = 0

        with open(archivo_filtrado_segundo, 'w', encoding='latin-1', newline='') as file:
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


    def get_diferencia(self, txt, pdf) -> bool:
        """
        True: txt tiene mas cantidad.
        False: pdf tiene mas cantidad\n
        """
        if len(txt) > len(pdf):
            return True
        else:
            return False

    # def igual_o_diferente(self, ruta_txt:str, ruta_pdf:str):
    #     """
    #     RESULTADO:
    #     Si hay igual cantidad de lineas en txt que pdf no hace nada,
    #     si  no, si hay mas pdf, los compara con el txt y los filtra a una carpeta.\n
    #     Si hay mas registros en el txt los compara con los pdf y filtra por segunda
    #     vez el txt.
    #     """

    #     txt = self.filtrar_txt_nuevo(ruta_txt)[0]
    #     pdf = self.nombres_pdf(ruta_pdf)
    #     self.generar_txt(ruta_txt)

    #     print(len(txt))
    #     print(len(pdf))

    #     if len(txt) == len(pdf):
    #         return 'hay misma cantidad de pdf y registros en txt'
    #     elif self.get_diferencia(txt, pdf):
    #         self.mas_txt(ruta_txt, pdf)
    #         return 'txt tiene mas'
    #     else:
    #         self.mas_pdf(pdf, txt, ruta_pdf)
    #         pdf = self.nombres_pdf(ruta_pdf)
    #         self.mas_txt(ruta_txt, pdf)
    #         return 'pdf tiene mas'
        




if __name__ == '__main__':

    asd = Datos()

    # nombres_txt = asd.nombres_txt(r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\RC\RC_1000015360_20221010060217.txt')
    # nombres_pdf = asd.nombres_pdf(r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\1000015360')

    # print(asd.igual_o_diferente(
    #     r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\RC\RC_1000015360_20221010060217.txt',
    #     r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\filtro_rc_fernando\archivos_fuente\1000015360',
    #     )
    # )
    
    print(asd.igual_o_diferente(
        r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\xprueba\rc\nuevo.txt',
        r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\xprueba\1',
        )
    )

