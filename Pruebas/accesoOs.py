import os



#  Creamos directorio Temp para descargar las actualizaciones SI no existe
def CrearBAT(config, app):
    path = config['Ruta']['RutaArranque']
    cmd = '@ECHO OFF\nCLS\nCD C:\AppData\Espacio\nActualizar.exe\nREPLACE Temp\*.* > Nul\nRD /s /q Temp > Nul\nMaster.exe\nEXIT'
    try:
        with open(path + config['Ruta']['NombreArranque'], 'w') as f:
            f.write(cmd)
        return 'Ok'
    except PermissionError:
        input('Se necesita permiso de administrador')
        return 'Error'


#  Creamos directorio Temp para descargar las actualizaciones SI no existe
def ExisteRuta(path, inicio=''):
    try:
        os.stat(path)
        existe = True
    except:
        if inicio == '':
            os.mkdir(path)
        existe = False
    if inicio == '':
        os.chdir(path)
    return existe


#  Creamos directorio Temp para descargar las actualizaciones SI no existe
def IrTemp(config, app):
    path = config['Ruta']['ruta'] + app + '\\Temp'
    ExisteRuta(path)


#  Comprobar si la app está instalada, sino lo está, INSTALA la app
def ExisteApp(config, app):
    path = config['Ruta']['ruta'] + app
    if not ExisteRuta(path, inicio= 'Si'):
        bat = CrearBAT(config, app)
        if bat == 'Ok':
            ExisteRuta(path)
        return bat
    else:
        return 'Si'