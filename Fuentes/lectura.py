# -*- coding: utf-8 -*-

import os, time, sys
from stat import *

# Paquetes del proyecto
import memoria 	as m		# Contiene las Clases Unidad / Directorio / Fichero
import mapeo	as c		# Contien funciones para mapear una línea de un fichero, mapear palabras


tipos = {'.py':'Python', '.pyc':'Python', '.txt':'texto', '.jpg':'foto', '.mp4':'video', '.doc':'documento','.docx':'documento',
		'.xls':'Excel', '.xlsx':'Excel', '.csv':'Excel', '.ppt':'presentacion', '.pptx':'presentacion', '.pdf':'pdf', '':'vacio',
		'.exe':'ejecutable', '.sqlite':'BDSqlite'} 
sintipo = []


tmp = u'.\\Tmp\dirtmp.txt'



def leer(ruta):
	# Comenzamos leyendo la información de la Unidad, la extraemos de hacer un DIR de DOS de la ruta dada
	unidad = leerunidad(ruta)
	
	leer_dir(unidad.directorio)
	act_directorio(unidad.directorio)
	
	return unidad


def leerunidad(ruta):
	# Utilizamos OS.POPEN para ejecutar comandos de DOS, en este cado hacemos un DIR de la ruta dada.
	inst_dos = 'dir ' + ruta + ' > ' + tmp
	f = os.popen(inst_dos)
	f.close()

	with open(tmp, 'rb') as f:
		# Las dos primeras líneas contienes el volumen y el número de serie (clave de las unidades)
		vol = c.leerlinea(f)[30:]		# extraemos el nombre del volumen de la línea 1
		nserie = c.leerlinea(f)[36:]	# extraemos el numero de serie (clave) de la linea 2
		fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		
		while True:
			linea = c.leerlinea(f)
			
			if linea == '':
				break	# Hemos llegado al final del fichero y salimos del bucle
			
			elif linea.find('dirs') != -1:
				libre = int(linea[23:linea.find('bytes')].replace(" ","").replace(".",""))
			
		# Creamos la clase Unidad con la información que tenemos
		unidad = m.Unidad(nserie, vol, libre, fechaudit)
		unidad.directorio = m.Directorio(ruta, '', 0, 0, 0, '')
	return unidad



def leer_dir(directorio):
	archivos, directorios, error = leer_ruta(directorio.path)
	
	numdir, numfile, tamano, fechamod = 0,0,0, ''
	for file in archivos:
		nom, ext, t, fmod, tam, erfile = leerfile(directorio.path, file)
		fichero = m.Fichero(nom, ext, t, fmod, tam, erfile)
		directorio.ficheros.append(fichero)
		
		numfile += 1
		tamano += fichero.tamano
		
		if fechamod < fichero.fechamod:
			fechamod = fichero.fechamod
		
	for dir in directorios:
		subdirectorio = m.Directorio(dir, '', 0, 0, 0, '')
		directorio.subdirectorios.append(subdirectorio)

		leer_dir(subdirectorio)
		numdir += 1
	
	directorio.numfiles = numfile
	directorio.tamano = tamano
	directorio.fechamod = fechamod
	directorio.error = error



def leer_ruta(ruta):
	files, subdir, error, file = [], [], '', ''
	try:
		listdirs = []
		listdirs = os.listdir(ruta)
	except PermissionError:
		#print ('ruta: ', ruta, ' Acceso denegado')
		error = ' (Acceso Denegado)'		
		return files, subdir, error
	
	for file in listdirs:
		try:
			pathname = os.path.join(ruta, file)
			if os.path.isdir(pathname):		# Tratamiento de subdirectorios
				subdir.append(pathname)
			else:							# Tratamiento de archivos
				files.append(file)
		except:
			print ('ruta: ', ruta, ' file: ', file, ' Error en ISDIR o ISFILE')
			error = ' (Error ISDIR o ISFILE)'		
			return files, subdir, error

	return files, subdir, error



def act_directorio(directorio):
	for dir in directorio.subdirectorios:
		act_directorio(dir)
		directorio.numfiles += dir.numfiles
		directorio.numdir += dir.numdir + 1
		directorio.tamano += dir.tamano
		if directorio.fechamod < dir.fechamod:
			directorio.fechamod = dir.fechamod



def leerfile(ruta, archivo):
	nombre, extension = os.path.splitext(archivo)
	nombre_completo = os.path.join(ruta, archivo)
	
	error, tipo = '', ''
	if extension.lower() in tipos:
		tipo = tipos[extension.lower()]
	elif not extension.lower() in sintipo:
		sintipo.append(extension.lower())

	try:
		tamano, fechamod = 0, ''
		e = os.stat(nombre_completo)
		tamano = e.st_size
		fechamod = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.st_mtime))
	except PermissionError:
		#print ('file: ', nombre_completo, ' Acceso denegado')
		error = ' (Acceso Denegado)'
	
	return nombre, extension, tipo, fechamod, tamano, error



	
if __name__ == "__main__":
	print ('-' * 70)
	leerdir(sys.argv[1])
