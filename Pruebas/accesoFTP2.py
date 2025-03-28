#  Conexión FTP: Conexión servidor
#  ===============================
from ftplib import FTP, all_errors, error_perm
import os
#from funciones import *



    def comprobarActualizacion(self):
        version = self.ftp.obtenerVersion(self.app)
        if version != self.version:
            #print("Hay versión nueva: ", version)
            return True
        else:
            #print("No hay versión nueva", version)
            return False




#  Creamos una clase conexionFTP a partir de la clase FTP
class conexionFTP(FTP):
    def __init__(self, servidor, usuario, password, puerto=21):
        super().__init__()
        self.connect(servidor, puerto)
        self.login(usuario, password)

    #  FUNCIONES BÁSICAS
    def cambiarDirectorio(self, directorio):
        try:
            self.cwd(directorio)
            return True
        except all_errors as e:
            print(f'Error FTP: {e}')
            return False

    def listar(self):
        try:
            return self.nlst()
        except all_errors as e:
            print(f'Error FTP: {e}')
            return []

    def subir(self, filename, callback=None):
        try:
            with open(filename, "rb") as f:
                self.storbinary("STOR " + filename, f, callback=callback)
        except all_errors as e:
            print(f'Error FTP: {e}')

    def bajar(self, filename, callback=None):
        cmd = "RETR " + filename
        try:
            if callback is None:        # Usar la callback por defecto
                with open('Espacio/' + filename, "wb") as f:
                    self.retrbinary(cmd, f.write)
            else:                       # Callback del usuario
                self.retrbinary(cmd, callback)
        except all_errors as e:
            print(f'Error FTP: {e}')
    
    

    #    FUNCIONES PROYECTO
    #  Obtener versión de Espacio
    def obtenerVersion(self, fichero):
        if self.cambiarDirectorio(fichero):
            for f in self.listar():
                #nombre, ext = Separar_nombre_extension(f)
                nombre, ext = os.path.splitext(f)
                if nombre[:len(fichero)] == fichero and ext == '.exe':
                    return nombre[len(fichero)+2:]
        else:
            return 0
    
    def descargarCredenciales(self):
        if self.cambiarDirectorio("Espacio"):
            cmd = "RETR Credenciales.json"
            try:
                with open('Credenciales.json', "wb") as f:
                    self.retrbinary(cmd, f.write)
            except all_errors as e:
                print(f'Error FTP: {e}')
        else:
            return 0