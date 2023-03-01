import os
import glob
import datetime
from generales.settings import ESTADOS
from dppsv.consultas import get_codigo_negocio_info
from dppsv.consultas import update_rc_info
from dppsv.consultas import get_last_rc_id
from dppsv.consultas import update_devolucion_pdf

ruta_pdfs = r'C:\Users\hcapra\Desktop\Nueva carpeta'
ruta_rc = r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\xprueba\rc\RC_1000015360_20221010060217.txt'

def get_date_rc(ruta_rc):
    head, archivo = os.path.split(ruta_rc)
    archivo = archivo[:-4].split('_')[-1]
    year    = archivo[0:4]
    mes     = archivo[4:6]
    dia     = archivo[6:8]
    hora    = archivo[8:10]
    minutos = archivo[10:12]
    segundos= archivo[12:14]

    fecha_hora_rc = f'{year}-{mes}-{dia} {hora}:{minutos}:{segundos}'
    fecha_hora_rc = datetime.datetime.strptime(fecha_hora_rc, '%Y-%m-%d %H:%M:%S')

    return fecha_hora_rc

def get_codigos_negocio(ruta_pdfs) -> list:

    pdf_nombres = glob.glob(os.path.join(ruta_pdfs, '*.pdf'))
    codigos_negocio = []

    for pdf in pdf_nombres:
        padre, nombre = os.path.split(pdf)
        dato = nombre.split('_')[-1].split('.')[0]
        codigos_negocio.append(dato)

    codigos_negocio.sort()

    return codigos_negocio

def insertar_codigos_info(ruta_pdfs, ruta_rc):

    update_rc_info(get_date_rc(ruta_rc))

    rc_id = get_last_rc_id()

    codigos = get_codigos_negocio(ruta_pdfs)

    
    for codigo in codigos:
        try:
            info        = get_codigo_negocio_info(codigo)
            try:
                codigo_id   = info[0]
                codigo_expo = info[1]
                update_devolucion_pdf(rc_id, codigo_expo, codigo_id, ESTADOS['estado_presuncion'])
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        
    print('Codigos de negocio ingresados en DEVOLUCION_PDF_DPPSV')


if __name__ == '__main__':
    ruta_pdfs = r'C:\Users\hcapra\Desktop\Nueva carpeta'
    ruta_rc = r'C:\Users\hcapra\Desktop\prueba_rc4\archivos\archivos_fuente_filtro_fernando\xprueba\rc\RC_1000015360_20221010060217.txt'

    insertar_codigos_info(ruta_pdfs, ruta_rc)