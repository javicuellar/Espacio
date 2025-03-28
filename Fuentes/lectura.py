# -*- coding: utf-8 -*-

import os, time, sys
from stat import *

# Paquetes del proyecto
import mapeo	as c		# Contien funciones para mapear una línea de un fichero, mapear palabras


tipos = {'.py':'Python', '.pyc':'Python', '.txt':'texto', '.jpg':'foto', '.mp4':'video', '.doc':'documento','.docx':'documento',
		'.xls':'Excel', '.xlsx':'Excel', '.csv':'Excel', '.ppt':'presentacion', '.pptx':'presentacion', '.pdf':'pdf', '':'vacio',
		'.exe':'ejecutable', '.sqlite':'BDSqlite'} 
sintipo = []


tmp = u'.\Espacio\Tmp\dirtmp.txt'



def Leer_unidad(ruta):
	# Utilizamos OS.POPEN para ejecutar comandos de DOS, en este cado hacemos un DIR de la ruta dada.
	inst_dos = 'dir ' + ruta + ' > ' + tmp
	f = os.popen(inst_dos)
	f.close()

	with open(tmp, 'rb') as f:
		# Las dos primeras líneas contienes el volumen y el número de serie (clave de las unidades)
		volumen = c.leerlinea(f)[30:]		# extraemos el nombre del volumen de la línea 1
		libre = 0
		fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		
		while True:
			linea = c.leerlinea(f)
			
			if linea == '':
				break	# Hemos llegado al final del fichero y salimos del bucle
			
			elif linea.find('dirs') != -1:
				libre = int(linea[23:linea.find('bytes')].replace(" ","").replace(".",""))
			
	return volumen, libre, fechaudit



def Leer_ruta(ruta):
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





def Leer_file(ruta, archivo):
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
	except FileNotFoundError:
		#print ('file: ', nombre_completo, ' Fichero no encontrado')
		error = ' (No encontrado)'
	
	return nombre, extension, tipo, fechamod, tamano, error



	
if __name__ == "__main__":
	pass
