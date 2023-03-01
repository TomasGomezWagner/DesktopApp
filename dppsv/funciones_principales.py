from dppsv.get_info import Datos
from generales.alertas import Alerts

# from codigos_negocio import insertar_codigos_info

def igual_o_diferente(ruta_txt:str, ruta_pdf:str):
    """
    RESULTADO:
    Si hay igual cantidad de lineas en txt que pdf no hace nada,
    si  no, si hay mas pdf, los compara con el txt y los filtra a una carpeta.\n
    Si hay mas registros en el txt los compara con los pdf y filtra por segunda
    vez el txt.\n
    Finalmente inserta la informacion de las presunciones en la tabla DEVOLUCION_PDF_DPPSV.
    """
    datos = Datos()
    txt = datos.filtrar_txt_nuevo(ruta_txt)[0]
    pdf = datos.nombres_pdf(ruta_pdf)
    datos.generar_txt(ruta_txt)


    if len(txt) == len(pdf):
        # insertar_codigos_info(ruta_pdf, ruta_txt)
        print('hay misma cantidad de pdf y registros en txt')
    
    elif datos.get_diferencia(txt, pdf): # txt tiene mas
        datos.mas_txt(ruta_txt, pdf)
        # insertar_codigos_info(ruta_pdf, ruta_txt)

    else: # pdf tiene mas
        datos.mas_pdf(pdf, txt, ruta_pdf)
        pdf = datos.nombres_pdf(ruta_pdf)
        datos.mas_txt(ruta_txt, pdf)
        # insertar_codigos_info(ruta_pdf, ruta_txt)

    # la funcion insertar_codigos_info no esta pudiendo conectarse a la base 
    # de datos del cecasit porque no tiene los puertos abiertos.
    # puede llegar a conectarse a la base que esta en CLARO, pero por ahora
    # esa no estaria sirviendo.

    Alerts.informacion()
