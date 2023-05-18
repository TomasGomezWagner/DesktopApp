from dppsv.get_info import Datos

def igual_o_diferente(ruta_txt:str, ruta_pdf:str) -> str:
    """
    RESULTADO:\n
    Si hay igual cantidad de lineas en txt que pdf solo retorna 'iguales'.\n
    Si hay mas pdf, los compara con el txt y los filtra a una carpeta. Retorna 'txt'.\n
    Si hay mas registros en el txt los compara con los pdf y filtra por segunda vez el txt. Retorna 'pdf'.
    """
    # Finalmente inserta la informacion de las presunciones en la tabla DEVOLUCION_PDF_DPPSV.

    datos   = Datos()
    txt     = datos.filtrar_txt_nuevo(ruta_txt, ruta_pdf)[0]
    pdf     = datos.nombres_pdf(ruta_pdf)

    datos.generar_txt(ruta_txt, ruta_pdf)

# ----------------------------------- IGUALES----------------------------------------------------
    if len(txt) == len(pdf):
        return 'iguales'
         
# ----------------------------------- MAS EN TXT ------------------------------------------------
    elif datos.get_diferencia(txt, pdf):
        datos.mas_txt(ruta_txt, pdf)
        return 'txt'
            
# ----------------------------------- MAS EN PDF ------------------------------------------------
    else: 
        datos.mas_pdf(pdf, txt, ruta_pdf)
        return 'pdf'
        
        


    
