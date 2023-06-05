import pymysql
from generales.settings import PRODUCCION as CONEXION

CONECTAR = pymysql.connect(
    host    = CONEXION['hostname'],
    user    = CONEXION['username'],
    passwd  = CONEXION['password'],
    db      = CONEXION['database'],
    #charset = CONEXION['charset'],
    port    =CONEXION['port'],
)

def get_one(conn, query):
    """ ejecuta query y retorna un solo valor en forma de tupla"""

    cur = conn.cursor()
    cur.execute(query)
    resultado = cur.fetchone()
    cur.close()

    return resultado

def get_many(conn, query):
    """ ejecuta query y retorna todos los valores, en forma de tupla"""

    cur = conn.cursor()
    cur.execute(query)
    resultado = cur.fetchall()
    cur.close()

    return resultado

# ------------------------------------------------------------------------------------------------------------------    

def get_negocio_data(codigo_negocio):
    """Busca por codigo de negocio en la tabla presuncion y retorna expo, protocolo y serie"""

    query = f'select expo_nro, protocolo, idprotocolo, serie FROM presuncion WHERE codigo_negocio = {codigo_negocio}'

    data = get_one(CONECTAR, query)

    return data



def get_expos(tabla:str, columna:str):
    """Devuelve una lista de las expos que contienen las notificaciones\n
    ingresadas a devolucion_pdf"""

    query = f'SELECT {columna} FROM {tabla} GROUP BY {columna};'
    
    datos = get_many(CONECTAR, query)
    expos = []

    for dato in datos:
        expos.append(dato[0])

    return expos



def contar(expos:list, tabla:str, columna:str):
    """Cuenta la cantidad de registros que tiene una exportacion\n
    que viene por parametro en una lista.\n
    Devuelve un diccionario con el numero de expo como key y cantidad como valor."""

    datos = {}
    for exportacion in expos:
        query = f"SELECT COUNT({columna}) FROM {tabla} WHERE {columna} = {exportacion} "

        cantidad = get_one(CONECTAR, query)
        datos[exportacion] = cantidad[0]

    return datos


def get_codigo_negocio_info(codigo_negocio):
    """ 
    Devuelve el id y expo en la tabla presunciones, correspondiente al codigo de negocio consultado\n
    [0] = id\n
    [1] = expo
    """

    query = f"SELECT id, expo_nro FROM presuncion WHERE codigo_negocio = {codigo_negocio}"

    datos = get_one(CONECTAR, query)

    return datos


def update_devolucion_pdf(id_rc, expo, id_presuncion, estado):

    query = f'INSERT INTO devolucion_pdf_dppsv (id_rc, expo, id_presuncion, estado) VALUES ({id_rc}, {expo}, {id_presuncion}, {estado})'

    cur = CONECTAR.cursor()
    cur.execute(query)
    CONECTAR.commit()
    print('codigo de negocio ingresado')


def update_rc_info(fecha_hora_rc):
    
    query = 'INSERT INTO devolucion_rc_dppsv (fecha_rc_disponible) VALUES ("%s")' % fecha_hora_rc
    cur = CONECTAR.cursor()
    cur.execute(query)
    CONECTAR.commit()
    print('ingresada la informacion del rc')

def get_last_rc_id():

    query = "SELECT MAX(id) from devolucion_rc_dppsv"
    ultimo_rc = get_one(CONECTAR, query)

    return ultimo_rc[0]

# print(contar(get_expos('devolucion_pdf', 'expo'), 'devolucion_pdf', 'expo'))
# print(contar(get_expos('presuncion', 'expo_nro'), 'presuncion', 'expo_nro'))

# print(get_codigo_negocio_info('26668991'))
