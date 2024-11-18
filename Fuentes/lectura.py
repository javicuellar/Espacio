# -*- coding: utf-8 -*-

import os, time
from stat import *

# Paquetes del proyecto
import memoria 	as m		# Contiene las Clases Unidad / Directorio / Fichero


tipos = {'.py':'Python', '.pyc':'Python', '.txt':'texto', '.jpg':'foto', '.mp4':'video', '.doc':'documento','.docx':'documento',
		'.xls':'Excel', '.xlsx':'Excel', '.csv':'Excel', '.ppt':'presentacion', '.pptx':'presentacion', '.pdf':'pdf', '':'vacio',
		'.exe':'ejecutable', '.sqlite':'BDSqlite'} 
sintipo = []


dicbyte = { b'\x81' : b'u',	 b'\xa6' : b'a', b'\xad' : b'!', 	# caractéres no válidos
			b'\xa0' : b'\xe1',	# á
			b'\x82' : b'\xe9',	# é
			b'\xa1' : b'\xed',	# í
			b'\xa2' : b'\xf3',	# ó
			b'\xa3' : b'\xfa', 	# ú
			b'\xa4' : b'\xf1' 	# ñ
			}

fec_display = '%Y-%m-%d %H:%M:%S'   # establece formato de fecha-hora


tmp = u'.\Tmp\dirtmp.txt'



def leer(ruta):
	# Comenzamos leyendo la información de la Unidad, la extraemos de hacer un DIR de DOS de la ruta dada
	unidad = leerunidad(ruta)
	
	directorio = m.Directorio(ruta, '', 0, 0, 0)
	unidad.directoro = directorio
	
	leer_dir(directorio)
	
	return unidad


def leerunidad(ruta):
	# Utilizamos OS.POPEN para ejecutar comandos de DOS, en este cado hacemos un DIR de la ruta dada.
	inst_dos = 'dir ' + ruta + ' > ' + tmp
	f = os.popen(inst_dos)
	f.close()

	with open(tmp, 'rb') as f:
		# Las dos primeras líneas contienes el volumen y el número de serie (clave de las unidades)
		vol = leerlinea(f)[30:-1]		# extraemos el nombre del volumen de la línea 1
		nserie = leerlinea(f)[36:-1]	# extraemos el numero de serie (clave) de la linea 2
		fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		
		while True:
			linea = leerlinea(f)
			
			if linea == '':
				break	# Hemos llegado al final del fichero y salimos del bucle
			
			elif linea.find('dirs') != -1:
				libre = int(linea[23:linea.find('bytes')].replace(" ","").replace(".",""))
			
	# Creamos la clase Unidad con la información que tenemos
	return m.Unidad(nserie, vol, libre, fechaudit)



def leer_dir(directorio):
	archivos, directorios, error = leer_ruta(directorio.path)
	
	numdir, numfile, tamano, fechamod = 0,0,0, ''
	for file in archivos:
		nom, ext, t, fmod, tam = leerfile(directorio.path, file)
		fichero = m.Fichero(nom, ext, t, fmod, tam)
		directorio.ficheros.append(fichero)
		
		numfile += 1
		tamano += fichero.tamano
		
		if fechamod < fichero.fechamod:
			fechamod = fichero.fechamod
		
	for dir in directorios:
		subdirectorio = m.Directorio(dir, '', 0, 0, 0)
		directorio.subdirectorios.append(subdirectorio)

		leer_dir(subdirectorio)
		numdir += 1
		#numdir += d
		#f = f + e
		#tablas.Grabardir((numserie, dir, f, c, d, p, fechaudit))
					#(numserie, path, fechamod, numfiles, numdir, tamano, fechaudit)
		#tamano += p
		#numfile += c
		#fechamod = f
	#print ('      Directorio: ', path)					# debug directorio leido
	print ('> Directorio: ', directorio.path, '  Num. files: ', numfile, '  Num. dir: ', numdir, '  Peso: ', tamano)	# debub num. archivos y tamano



def leer_ruta(ruta):
	files, subdir, error = [], [], ''
	try:
		for file in os.listdir(ruta):
			pathname = os.path.join(ruta, file)
			info = os.stat(pathname)
			if S_ISDIR(info.st_mode):    	# Tratamiento de subdirectorios
				subdir.append(pathname)
			elif S_ISREG(info.st_mode):  	# Tratamiento de archivos
				files.append(file)
			else:				 			# desconocido tipo de fichero
				print (' > Fichero desconocido %s' % pathname)
	except PermissionError:
			error = ' (Acceso Denegado)'
	return files, subdir, error


def leerlinea(file):
	linea, byte = '', b' '
	byte = file.read(1)
	while byte != b'' and byte != b'\r':
		if byte in dicbyte:
			# caracter transformado que da error o es invalido
			byte = dicbyte[byte]
		linea += byte.decode(u'cp1252')
		byte = file.read(1)
	#print (' > ', linea)
	return linea


def calculardirectorio(directorio, ruta):
	num_subdir = len(directorio.subdirectorios) - 1
	subdir = directorio.subdirectorios
	
	for dir in range(num_subdir, -1, -1):
		if ruta.find(subdir[dir].path) == 0:
			return calculardirectorio(subdir[dir], ruta)
	return directorio
		


def actdirectorio(directorio):
	for dir in directorio.subdirectorios:
		actdirectorio(dir)
		directorio.numfiles += dir.numfiles
		directorio.numdir += dir.numdir + 1
		directorio.tamano += dir.tamano



def leerfile(ruta, archivo):
	nombre, extension = os.path.splitext(archivo)
	nombre_completo = os.path.join(ruta, archivo)
	e = os.stat(nombre_completo)

	tamano = e.st_size
	fechamod = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.st_mtime))

	tipo = ''
	if extension.lower() in tipos:
		tipo = tipos[extension.lower()]
	elif not extension in sintipo:
		sintipo.append(extension)
	
	#print ('   --> ', nombre_completo, '    ', fechamod, ' ', tamano, ' ', tipo)	# debug archivos
	return nombre, extension, tipo, fechamod, tamano



	
if __name__ == "__main__":
	print ('-' * 70)
	leerdir(sys.argv[1])
