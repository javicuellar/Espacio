###################################################################################################################################
#  Proyecto: ESPACIO, Módulo MASTER - Módulo director para ejecución del proyecto Espacio 
#  ========================================================================================
app = 'Espacio'
modulo = 'Master'
#    ---------------------------------------
version = '6.03'
#       * Se modifica el módulo para ejecutar los scripts con os.popen y grabar la salida en TMP
#       * Se envian todos los ficheros del directorio TMP al Servidor (las salidas de las ejecuciones y los que se hayan generado)
#       * Se incluye la función Actualziar para actualizar todos los módulos del proyecto (fichero configuración y Espacio)
#       * Se corrigen errores en Instalar: se crea directorio TMP inicialmente, se descarga también Master.exe, mensaje error si 
#       se instala sin permisos de Administrador.
#
# version = '5.341'
#       * Limpiamos la versión 5.34 = 0.34, dejando únicamente los fuentes necesarios
#
# version = '0.31'
#       * Se modifica fichero de configuración para coger uno de pruebas.
#       * Se modifica el módulo a ejecutar en la configuración para añadir la extensión
#
# version = '0.2'
#       * Módulo LeerConfig - Se incorpora csv con configuración. Leer con pandas y crear diccionario configuración
#       * Lectura del directorio de trabajo de configuración
#       * Leer los módulos a ejecutar de la configuración
#       * Se incorpora funcionalidad para actualizar el módulo Actualizar
#
# version = '0.0'
#       * Define el directorio de trabajo y se posiciona en él 
#       * Ejecución del módulo Espacio, lectura y análisis de dispositivos conectados
#           - los módulos a ejecutar deben estar parametrizados en la Configuración, inicialmente están en el código
###################################################################################################################################
from leerConfig import LeerConfig

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


#  Enviar ficheros generados en directorio Tmp al Servidor
def Enviar_FTP(ftp, local, remoto):
    try:
        ftp.cwd(remoto)
    except:
        print("Se ha producido un error al acceder al directorio del Servidor ", remoto, "  Posicionado en dir. remoto: ", ftp.pwd())
        return

    # Obtener la lista de archivos y directorios en el directorio local
    contenido_local = os.listdir(local)

    for elemento in contenido_local:
        ruta_local = os.path.join(local, elemento)
        if os.path.isfile(ruta_local):
            # Es un archivo, enviarlo por FTP
            with open(ruta_local, 'rb') as archivo:
                ftp.storbinary('STOR ' + elemento, archivo)
        elif os.path.isdir(ruta_local):
            # Es un directorio, crearlo en el servidor remoto y enviar su contenido
            ftp.mkd(elemento)
            Enviar_FTP(ftp, ruta_local, elemento)


#  Actualizar módulos del proyecto
def Actualizar(modulo):
    #  Comprobar si existe la ruta (directorio)
    def ExisteRuta(ruta):
        try:
            os.stat(ruta)
            return True
        except:
            return False
    
    #  Crear directorio de la app y ficheros de ejecución y arranque en Inicio
    def Instalar(path):
        ruta = config['Ruta']['RutaArranque']
        cmd = 'cscript ' + path + app + '.vbs'
        try:
            with open(ruta + config['Ruta']['NombreArranque'], 'w') as f:
                f.write(cmd)
        except PermissionError:
            print('Se necesita permiso de administrador')
            return False
    
        try:
            os.mkdir(path)
        except:
            pass
        try:
            os.mkdir(path + app)
        except:
            pass
        try:
            os.mkdir(path + app + '\Tmp')
        except:
            pass

        cmd = 'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "' + path + app + '.bat" & Chr(34), 0\nSet WshShell = Nothing'
        try:
            with open(path + app + '.vbs', 'w') as f:
                f.write(cmd)
        except PermissionError:
            pass

        cmd = '@ECHO OFF\nCLS\nCD ' + path + app + '\nMaster.exe'
        try:
            with open(path + app + '.bat', 'w') as f:
                f.write(cmd)
        except PermissionError:
            pass

        return True


    #  Comprobar si la app está instalada, sino lo está, INSTALAR la app
    path = config['Ruta']['ruta']
    
    instalar = True
    if not ExisteRuta(path + app):
        instalar = Instalar(path)
        if instalar:
            modulo = 'Instalar'
    
    if instalar:
        os.chdir(path + app)
        version = config['Version'][app]

        #  Conexión FTP - Descargar ficheros del directorio app
        DescargarFTP(ftp, version, modulo)

    return instalar





# ------------------------------------------------------------------------------------------------------------------------------------
print("Script Master - Versión", version)

config = LeerConfig(app)

#  Conexión al Servidor FTP para Actualizar
ftp = ConectarFTP()
estado = Actualizar(modulo)


if estado:
    equipo = getattr(platform, 'node')()

    #  Ejecutamos los módulos parametrizados en la Configuración
    for script in config['Master']:
        if config['Pruebas']['Entorno'] == 'Pruebas':
            salida = equipo + '-' + config['Master'][script] + '.out'
        else:
            salida = equipo + '-' + script + '.out'
        
        cmd = script + ' > .\Tmp\\' + salida
        f = os.popen(cmd)
        f.close()

    
    if equipo == config['Ruta']['NAS']:
        #  Tratamiento de los datos leídos (y descargados del Servidor) y grabación en BBDD
        for script in config['Analisis']:
            if config['Pruebas']['Entorno'] == 'Pruebas':
                salida = equipo + '-' + config['Analisis'][script] + '.out'
            else:
                salida = equipo + '-' + script + '.out'
        
            cmd = script + ' > .\Tmp\\' + salida
            f = os.popen(cmd)
            f.close()
    else:
        #  Enviar ficheros generados en directorio Tmp al Servidor
        origen  = '.\Tmp\\'
        destino = '/' + app + '/Tmp'
        Enviar_FTP(ftp, origen, destino)

ftp.quit()