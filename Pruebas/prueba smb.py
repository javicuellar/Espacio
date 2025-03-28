from smb.SMBConnection import SMBConnection
import os

def ConexionFTP(usuario, password, equipo, servidor):
	try:
		conn = SMBConnection(usuario, password, equipo, servidor)
		conn.connect(servidor)
		return conn
	except:
		print('Error - No es posible conectarse al Servidor', equipo)
		return


#   Información del DIRECTORIO en el Servidor vía SMB
def Leer_DirectorioSMB(conn, volumen, directorio, ruta, error=''):
	try:
		elementos = conn.listPath(directorio, ruta)
	except:
		print('Recurso no accesible')
		elementos = []

	path = os.path.normpath(directorio + ruta)
		
	tamaño = 0
	print("Directorio: ", directorio, " Ruta: ", ruta, " >", path)
	for elemento in elementos:
		if elemento.isDirectory:
			if elemento.filename not in ['.', '..']:
				# ruta = os.path.join(ruta, elemento.filename)
				tamaño += Leer_DirectorioSMB(conn, volumen, directorio, os.path.join(ruta, elemento.filename))
		else:
			nombre, extension = os.path.splitext(elemento.filename)
			tamañofich = elemento.file_size
			error = ''
			tamaño += tamañofich
			print("   > Fich: ", volumen, path, nombre, extension, tamañofich, error)

	print(" > Dir: ", volumen, path, tamaño, error)
	return tamaño


bd = ConexionFTP('Javi', 'Dcjavier9', 'NAS', 'javicu.synology.me')

# directorios = []
try:
    directorios = bd.listShares()              # obtain a list of shares
except:
    print('### can not list shares') 

for directorio in directorios:
	Leer_DirectorioSMB(bd, 'NAS', directorio.name, '/')