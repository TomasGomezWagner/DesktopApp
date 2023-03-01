
import os
import glob
from pathlib import Path
from funciones.manage_files import Manage
from gender_detector import gender_detector

class Filtros:

    def __init__(self) -> None:
        pass


    def filtro_vacios(registros:list[list]) ->dict:
        """
        Checkea si campos estan vacios y genera un diccionario\n
        con 'archivo_filtrado'.\n
        archivo_filtrado['ok'] = registros correctos.\n
        archivo_filtrado['errores'] = registros con errores.
        """

        archivo_filtrado        = {}
        registros_ok            = []
        con_errores             = []
        contador_sin_tipo       = 0 #56
        contador_sin_numero_doc = 0 #57
        contador_sin_nombre     = 0 #59
        contador_sin_apellido   = 0 #60
        contador_sin_razon      = 0 #61
        contador_sin_marca      = 0 #54
        contador_sin_modelo     = 0 #55
        contador_sin_provincia  = 0 #69
        contador_sin_partido    = 0 #70
        contador_sin_localidad  = 0 #71
        contador_cp             = 0 #72
        contador_longitud       = 0

        for row in registros:
            if len(row) > 74:
                row.append('tienen un punto y coma demas')
                contador_longitud += 1
                con_errores.append(row)
            elif row[0] != 'P':
                row.append('sin P al inicio')
                con_errores.append(row)
            elif row[56] == '':
                row.append('sin tipo de documento')
                contador_sin_tipo +=1
                con_errores.append(row)
            elif row[57] == '':
                row.append('sin numero de documento')
                contador_sin_numero_doc +=1
                con_errores.append(row)
            elif row[56]!= '4' and row[59] == '':
                row.append('sin nombre de titular')
                contador_sin_nombre +=1
                con_errores.append(row)
            elif row[56]!= '4' and row[60] == '':
                row.append('sin apellido de titular')
                contador_sin_apellido +=1
                con_errores.append(row)
            elif row[56] == '4' and row[61] == '':
                row.append('sin razon social')
                contador_sin_razon +=1
                con_errores.append(row)
            elif row[54] == '':
                row.append('sin marca de vehiculo')
                contador_sin_marca +=1
                con_errores.append(row)
            elif row[55] == '':
                row.append('sin modelo de vehiculo')
                contador_sin_modelo +=1
                con_errores.append(row)
            elif row[69] == '':
                contador_sin_provincia += 1
                row.append('sin provincia')
                con_errores.append(row)
            elif row[70] == '':
                contador_sin_partido += 1
                row.append('sin partido')
                con_errores.append(row)
            elif row[71] == '':
                contador_sin_localidad += 1
                row.append('sin localidad')
                con_errores.append(row)
            elif row[72] == '':
                contador_cp += 1
                row.append('sin codigo postal')
                con_errores.append(row)
            elif row[72] == '9999' or row[72] == '0':
                contador_cp += 1
                row.append('codigo postal 9999 o cero')
                con_errores.append(row)
            else:
                registros_ok.append(row)

        archivo_filtrado['ok']          = registros_ok
        archivo_filtrado['errores']     = con_errores
        print(len(archivo_filtrado['ok']), len(archivo_filtrado['errores']))
        return archivo_filtrado
            


    def filtro_documento(resultado_vacios:dict) -> dict:
        """
        Agrega a lista eliminados si: es cuit(4) y tiene mas de 11 numeros\n
        o si es diferente a 4 y tiene menos de 7 o mas de 8 caracteres.\n
        Si no tiene ninguno de esos errores, la linea, se agtrega a la lista ok.\n
        Genera un diccionario 'archivo_filtrado'.\n
        archivo_filtrado['ok'] = registros correctos.\n
        archivo_filtrado['errores'] = registros con errores.
        """        
        con_errores : list
        registros   : list 

        archivo_filtrado    = {}
        registros_ok        = []
        registros           = resultado_vacios['ok'] 
        con_errores         = resultado_vacios['errores']
        errores_doc_cant    = 0

        for row in registros:
            if row[56] == '4' and len(row[57]) != 11:
                row.append('cuit con error en cantidad')
                con_errores.append(row)               
            elif row[56] != '4' and ( len(row[57])<7 or len(row[57])>8 ):
                row.append('documento con cantidad erronea')
                con_errores.append(row)
            else:
                registros_ok.append(row)
        
        archivo_filtrado['ok']      = registros_ok
        archivo_filtrado['errores'] = con_errores
        print(len(archivo_filtrado['ok']), len(archivo_filtrado['errores']))
        return archivo_filtrado


    def verificar_sexo(resultado_filtrado:dict) -> dict :
        """
        Si el campo genero esta vacio o no es M o F y no es cuil, checkea si el primer nombre\n
        esta en la base de datos del modulo GenderDetector y completa segun resultado.\n
        Si el resultado es desconocido, agrega la linea a la lista de errores.\n
        Si el tipo de doc es cuil y no esta vacio o no es J, cambia el valor por J.\n
        Genera un diccionario 'archivo_filtrado'.\n
        archivo_filtrado['ok'] = registros correctos.\n
        archivo_filtrado['errores'] = registros con errores.
        """
        con_errores : list
        registros   : list 

        archivo_filtrado    = {}
        registros_ok        = []
        generos             = ['M', 'F', 'J']
        detector            = gender_detector.GenderDetector('uy')
        registros           = resultado_filtrado['ok'] 
        con_errores         = resultado_filtrado['errores']
        
        def remover(lista:list):
            """ Elimina si hay items vacios en la lista """
            for index, item in enumerate(lista):
                if item == '':
                    lista.pop(index)
                    remover(lista)

            return lista
        
        def recorrer_genero(nombres:list):
            try:
                genero = detector.guess(nombres[0])
                if genero == 'female':                    
                    row[58] = 'F'
                    registros_ok.append(row)
                elif genero == 'male':                    
                    row[58] = 'M'
                    registros_ok.append(row)
                else:
                    nuevo_nombres = nombres[1:]
                    recorrer_genero(nuevo_nombres)
            except IndexError:
                row.append('no se pudo determinar el genero')
                con_errores.append(row)
            except Exception as e:
                print(e)
                row.append('no se pudo determinar el genero')
                con_errores.append(row)
            

        for row in registros:
            if (row[56] != '4') and (row[58] == '' or row[58] not in generos):
                nombres = row[59].split(' ')
                
                remover(nombres) #elimina si hay espacios en blanco delante o detras
                
                recorrer_genero(nombres)
                
                # genero = detector.guess(nombres[0])
                
                # if genero == 'female':                    
                #     row[58] = 'F'
                #     registros_ok.append(row)
                # elif genero == 'male':                    
                #     row[58] = 'M'
                #     registros_ok.append(row)
                # else:
                #     if len(nombres)>1:
                        
                #         genero = detector.guess(nombres[1])    
                                         
                #         if genero == 'female':                           
                #             row[58] = 'F'
                #             registros_ok.append(row)
                #         elif genero == 'male':                           
                #             row[58] = 'M'
                #             registros_ok.append(row)
                #         else:
                #             row.append('no se pudo determinar el genero')
                #             con_errores.append(row)
                #     else:
                #         row.append('no se pudo determinar el genero')
                #         con_errores.append(row)

            elif (row[56] == '4') and (row[58] == '' or row[58] not in generos):
                row[58] = 'J'
                registros_ok.append(row)
            elif row[58] in generos:
                registros_ok.append(row)
            else:
                row.append('campo sexo diferente a F, M o J')
                con_errores.append(row) 
        
            
        archivo_filtrado['ok']      = registros_ok
        archivo_filtrado['errores'] = con_errores
        print(len(archivo_filtrado['ok']), len(archivo_filtrado['errores']))
        return archivo_filtrado


    def get_imagenes_a_borrar(datos_errores:list[list]) -> list:

        nombre_imagenes = []

        for row in datos_errores:
            nombre_imagenes.append(row[12])
            nombre_imagenes.append(row[37])
            nombre_imagenes.append(row[38])
            nombre_imagenes.append(row[39])
        
        return nombre_imagenes


    def modificar_txt_cantidad(ruta_txt_errores:str) -> None:
        """
        Modifica el archivo que contiene solo datos para el correo (el que finaliza con RN).\n
        Se coloca la cantidad que figura en el archivo filtrado y genera el archivo nuevo con \n
        el sufijo 'modificado'.
        """
        parent                  = Path(ruta_txt_errores).resolve().parent
        txt_cantidad            = glob.glob(os.path.join(parent, '*RN.txt'))
        txt_filtrado            = glob.glob(os.path.join(parent, '*filtrado.txt'))
        
        nombre_archivo_cantidad = txt_cantidad[0].split('.')[0]

        datos_txt_cantidad          = Manage.leer_archivo(txt_cantidad[0])
        cantidad_txt_filtrado       = len(Manage.leer_archivo(txt_filtrado[0]))

        datos_txt_cantidad[-1][-1]  = cantidad_txt_filtrado
        datos_txt_cantidad[-2][-1]  = cantidad_txt_filtrado
        
        Manage.make_archivo(
            datos_txt_cantidad,
            os.path.join(parent, f'{nombre_archivo_cantidad}-modificado.txt')
            )

        





if __name__ == '__main__':
    from manage_files import Manage
    archivo = Manage()
    filtro = Filtros()

    Filtros.modificar_txt_cantidad(r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\archvos_tar\M161-135-1-246993-ENFORCER_156-220722-errores.txt')

    # datos = archivo.leer_archivo(r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\M161-135-1-247674-ENFORCER_155-050822.txt')
    # filtrados = filtro.filtro_vacios(datos)
    # filtro_doc = filtro.filtro_documento(filtrados)
    # filtro_sex = filtro.verificar_sexo(filtro_doc)

    
    # archivo.make_archivo(filtro_sex['ok'],r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\ok.txt')
    # print('done')
    # archivo.make_archivo(filtro_sex['errores'],r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\errores.txt')
    # print('done')



