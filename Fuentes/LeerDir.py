###################################################################################################################################
#  Proyecto: ESPACIO, Módulo LeerDir - Análisis de ficheros con el DIR /s de la unidad. 
#  ========================================================================================
app = 'Espacio'
modulo = 'LeerDir'
#    ---------------------------------------
version = '6.04'
#       * Lee la información del Servidor (directorio Tmp) y la analiza para grabar en la BBDD
#           - Lectura de Dispositivos  (ficheros *.csv)
#           - Lectura de Unidades  (ficheros *-Unidades.csv)
#           - Lectura de los DIR /S de las Unidades  (ficheros *.txt)
#       * Tareas a realizar:
#           - Descargar ficheros del Servidor a Local y borrarlos
#           - Análisis de ficheros descargados y grabación en BBDD:
#               * Dispositivos  (ficheros *.csv)
#               * Unidades  (ficheros *-Unidades.csv)
#               * Unidades DIR /s  (ficheros *.txt)
###################################################################################################################################
from leerConfig import LeerConfig
from datetime import datetime

from ftplib import FTP, all_errors
import os, platform




#  Conexión al Servidor vía FTP
def ConectarFTP():
    ftp = 'FTP'
    servidor = config['Servidor']['servidor']
    usuario  = config[ftp]['usuario']
    password = config[ftp]['password']
    try:
        ftpEspacio = FTP()
        ftpEspacio.connect(servidor)
        ftpEspacio.login(usuario, password)
    except all_errors as e:
        print(f'Error FTP: {e}')
    return ftpEspacio


#   Descargar ficheros de la aplicación (directorio app)
def DescargarFTP(ftp, version, modulo):
    try:
        ftp.cwd(app)
        ficheros = []
        ftp.dir(ficheros.append)
        for f in ficheros:
            tipo = f[0]
            directorio = f[59:]
            if tipo == 'd':     # Es un directorio
                break
        
        if modulo == 'Master':
            appDisplay = 'Actualizar'
        else:
            appDisplay = app
        
        if modulo == 'Instalar' or directorio > version:
            print("Script Actualizar - Versión", appDisplay, version, "-> Versión Servidor", directorio)
            ftp.cwd(directorio)
            ficheros = []
            ftp.dir(ficheros.append)
            for f in ficheros:
                fichero = f[59:]
                if (modulo == 'Master' and fichero != 'Master.exe')     \
                or (modulo == 'Instalar'):
                    cmd = "RETR " + fichero
                    with open(fichero, "wb") as f:
                        ftp.retrbinary(cmd, f.write)
                #else:
                    #print("Fichero no descargado -> ", fichero, " - Módulo: ", modulo)
    except all_errors as e:
        print(f'Error FTP: {e}')





# ------------------------------------------------------------------------------------------------------------------------------------
print("Script ", modulo, " - Versión", version, "  ", datetime.now().strftime("%d/%m/%Y %H:%M"))

config = LeerConfig(app)

#  Conexión al Servidor FTP para Actualizar
ftp = ConectarFTP()

ftp.quit()