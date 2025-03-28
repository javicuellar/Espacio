###################################################################################################################################
#  Proyecto: ESPACIO, Módulo Espacio - Analizador de Dispositivo (unidades, directorios y ficheros)
#  =================================================================================================
app = 'Espacio'
#    Modulo Espacio - Versión inicial 0.0
#    ---------------------------------------
version = '6.03'
#       * Grabar los ficheros de salida en directorio TEMP y no enviar al Servidor. Enviar los ficheros con otro módulo (Master?)
# version = '6.022'
#       * Corregir error al leer unidades floppy. LeerUnidad devuelve lista vacía y no se añade a unidades.
# version = '6.02'
#       * Grabar dispositivos en formato CSV, con nombre de equipo
#       * Grabar dir (unidad) con nombre del volumen para que no se machaquen las unidades USB (las E:\)
# version = '6.01'
#       * Eliminada condición que únicamente subía la información al Servidor en entorno de Pruebas.
# version = '6.0'
#       * Cambiamos la versión inicial que baja BBDD, lee los dispositivo y los graba en BBDD para volver a subir al servidor, por
#       nueva versión más ligera. Únicamente genera fichero plano de las unidades haciendo dir /s sobre ellas y lo sube al servidor 
#       para ser procesado y grabado en BBDD posteriormente.
###################################################################################################################################
from leerConfig import LeerConfig
from datetime import datetime

import os, psutil, platform, time
import pandas as pd




def LeerDispositivo():
    equipo = getattr(platform, 'node')()
    sistema = getattr(platform, 'system')()
    so = getattr(platform, 'platform')()
    maquina = getattr(platform, 'machine')()
    arquitectura = getattr(platform, 'architecture')()[0]
    procesador = getattr(platform, 'processor')()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    disp = [[fecha, equipo, sistema, so, maquina, arquitectura, procesador]]
    cabeceras = ['fecha', 'equipo', 'sistema', 'so', 'maquina', 'arquitectura', 'procesador']
    df = pd.DataFrame(disp, columns=cabeceras)
    df.to_csv(equipo + '.csv', index=False)

    return (equipo, sistema)


def LeerUnidad(ruta, tipo):
    tiempo_ini = time.time()
    try:
        disco = psutil.disk_usage(ruta)
        total = disco.total
        usado = disco.used
        porcentaje = disco.percent
        libre = disco.free

        f = os.popen('dir ' + ruta)
        volumen = f.readline()[30:-1].upper()
        f.close()
        
        fichero = volumen + '.txt'
        cmd = 'DIR ' + ruta + '/a /o /-c /s > ' + fichero
        f = os.popen(cmd)
        f.close()
    except Exception as error:
        print("> error en unidad: ", ruta, " - ", error)
        return []
    
    seg = int(time.time() - tiempo_ini)
    tiempo = 'Tiempo lectura ' + ruta + '  ' + str(seg // 60) + "'" + str(seg % 60) + '"'
    return [volumen, ruta, tipo, total, usado, porcentaje, libre, tiempo]




# ------------------------------------------------------------------------------------------------------------------------------------
print("Script Espacio - Versión", version, "  ", datetime.now().strftime("%d/%m/%Y %H:%M"))

#  Carga de diccionarios de Configuración
config = LeerConfig(app)

if config != {}:
    path = config['Ruta']['tmp']
    try:
        os.mkdir(path)
    except:
        pass
    os.chdir(path)
    
    #  Analizar dispositivo
    equipo, sistema = LeerDispositivo()

    if sistema == 'Windows':
        unidades = []
        particiones = psutil.disk_partitions()
        for partición in particiones:
            unidad = LeerUnidad(partición.mountpoint, partición.fstype)
            if unidad != []:
                unidades.append(unidad)

    if unidades != []:
        cabeceras = ['volumen', 'ruta', 'tipo', 'total', 'usado', 'porcentaje', 'libre', 'tiempo']
        df = pd.DataFrame(unidades, columns=cabeceras)
        df.to_csv(equipo + '-Unidades.csv', index=False)