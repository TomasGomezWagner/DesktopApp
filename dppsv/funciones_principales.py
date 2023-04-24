from dppsv.get_info import Datos

def igual_o_diferente(ruta_txt:str, ruta_pdf:str) -> None:
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

# ----------------------------------- IGUALES----------------------------------------------------

    if len(txt) == len(pdf):
        datos.renombrar_filtrado(ruta_txt)
        #principal_codigo_negocio(ruta_pdf, ruta_txt)
        return 'iguales'
        
        
# ----------------------------------- MAS EN TXT ------------------------------------------------

    elif datos.get_diferencia(txt, pdf):
        datos.mas_txt(ruta_txt, pdf)
        #principal_codigo_negocio(ruta_pdf, ruta_txt)
        return 'txt'
        
        
# ----------------------------------- MAS EN PDF ------------------------------------------------

    else: 
        datos.mas_pdf(pdf, txt, ruta_pdf)
        datos.renombrar_filtrado(ruta_txt)
        #principal_codigo_negocio(ruta_pdf, ruta_txt)
        return 'pdf'
        
        


    
