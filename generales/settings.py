VERSION = '1.4.6' # 1.4.4 los antivirus detectan el exe como troyano

RUTA_VERSION = 'https://raw.githubusercontent.com/TomasGomezWagner/CecaitraApp/main/utils/version.txt'


LOCAL = {
    'hostname':'localhost',
    'database':'cecasit',
    'username':'tomy',
    'password':'123456',
    'charset':'latin1',
    'port':3306,
}

CECASIT = {
    'hostname':'cecasit.cecaitra.com',
    'port':3306,
    'database':'cecasit',
    'username':'cecasit',
    'password':'Yn3hCPGtAEL2QJyj',
}

CECASIT_PRODUCCION = {
    'hostname':'cecasit.ar',
    'port':50312,
    'database':'cecasit',
    'username':'lmila',
    'password':'lm2023',
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