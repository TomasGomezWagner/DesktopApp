VERSION = '1.4.7' # 1.4.4 los antivirus detectan el exe como troyano

RUTA_VERSION = 'https://raw.githubusercontent.com/TomasGomezWagner/CecaitraApp/main/utils/version.txt'


LOCAL = {
    'hostname':'localhost',
    'database':'cecasit',
    'username':'tomy',
    'password':'123456',
    'charset':'latin1',
    'port':3306,
}

DATABASE = {
    'hostname':'192.0.0.0',
    'port':3306,
    'database':'database',
    'username':'username',
    'password':'password',
}

PRODUCCION = {
    'hostname':'hostname',
    'port':'port',
    'database':'database',
    'username':'username',
    'password':'password',
}

ESTADOS = {
    'estado_presuncion':10,
}


MENSAJES = {
    'iguales':'Habia igual cantidad.\nSe generó:\nArchivo final\nArchivo salida',
    'txt':'Habia mas registros en el txt.\nSe generó:\nArchivo final\nArchivo salida',
    'pdf':'Habia mas PDFs que registros en el txt.\nSe generó:\nArchivo final\nArchivo salida\nCarpeta pdf_demas',
    'pdf_con_errores' :'\nRevisar porque no se pudo obtener la informacion de algun PDF.',
}